import React, { Component, RefObject } from "react";
import { withRouter } from "../../navigation/navigation-utils";
import { IdeaAppLayoutProps } from "../../components/app-layout";
import { IdeaSideNavigationProps } from "../../components/side-navigation";
import { Button, FlashbarProps, Link, TableProps } from "@cloudscape-design/components";
import { Role } from "../../client/data-model";
import IdeaListView from "../../components/list-view";
import AuthzClient from "../../client/authz-client";
import ProjectsClient from "../../client/projects-client";
import { AppContext } from "../../common";
import Utils from "../../common/utils";

export interface PermissionProfilesProps extends IdeaAppLayoutProps, IdeaSideNavigationProps { }

export interface PermissionProfilesState {
  profileSelected: boolean;
  selectedPermissionProfile: Role[];
  affectedProjects: Map<string, number>;
  roleCount: number;
}

class PermissionProfilesDashboard extends Component<PermissionProfilesProps, PermissionProfilesState> {
  listing: RefObject<IdeaListView>;

  constructor(props: PermissionProfilesProps) {
    super(props);
    this.listing = React.createRef();
    this.state = {
      profileSelected: false,
      selectedPermissionProfile: [],
      affectedProjects: new Map<string, number>(),
      roleCount: 0,
    };
  }

  authzClient(): AuthzClient {
    return AppContext.get().client().authz();
  }

  projectsClient(): ProjectsClient {
    return AppContext.get().client().projects();
  }

  setFlashbarMessage(type: FlashbarProps.Type, content: string, header?: React.ReactNode, action?: React.ReactNode) {
    this.props.onFlashbarChange({
      items: [
        {
          type,
          header,
          content,
          action,
          dismissible: true,
        }
      ]
    })
  }

  isSelected(): boolean {
    return this.state.profileSelected;
  }

  getSelectedPermissionProfile(): Role | null {
    return this.state.selectedPermissionProfile.length === 0 ? null : this.state.selectedPermissionProfile[0];
  }

  PERMISSION_PROFILES_TABLE_COLUMN_DEFINITIONS: TableProps.ColumnDefinition<Role>[] = [
    {
      id: "role_id",
      header: "Role ID",
      cell: (role) => <Link href={`/#/cluster/permissions/project-roles/${role.role_id}`}>{role.role_id}</Link>,
    },
    {
      id: "name",
      header: "Role name",
      cell: (role) => role.name,
    },
    {
      id: "description",
      header: "Description",
      cell: (role) => role.description || "-",
    },
    {
      id: "latestUpdate",
      header: "Latest update",
      cell: (role) => `${role.updated_on ? Utils.convertToRelativeTime(Number(role.updated_on)) : "-"}`,
    },
    {
      id: "affectedProjects",
      header: "Affected projects",
      cell: (role) => <Link
        href={`/#/cluster/permissions/project-roles/${role.role_id}`}
        onFollow={(event) => {
          event.preventDefault();
          this.props.navigate(`/cluster/permissions/project-roles/${role.role_id}`, {
            state: { activeTabId: "affected-projects" }
          });
        }}
      >
        {this.state.affectedProjects.get(role.role_id) ?? "0"}
      </Link>,
    },
  ];

  getListing(): IdeaListView {
    return this.listing.current!;
  }

  deleteProfile(): void {
    this.authzClient().deleteRole({
      role_id: this.state.selectedPermissionProfile[0].role_id,
    }).then((_) => {
      this.setFlashbarMessage("success", "1 project role deleted successfully. This deletion did not impact any ongoing projects.");
      this.setState(
        {
          profileSelected: false,
        },
        () => {
          this.getListing().fetchRecords();
        }
      );
    }).catch((e) => {
      this.setFlashbarMessage("error", "Failed to delete project role.");
    });
  }

  buildListing() {
    return (
      <IdeaListView
        ref={this.listing}
        preferencesKey={"permission-profiles"}
        showPreferences={true}
        title="Project roles"
        titleVariant="h2"
        counter={`(${this.state.roleCount})`}
        variant="container"
        selectionType="single"
        primaryAction={{
          id: "create-profile",
          text: "Create role",
          onClick: () => {
            this.props.navigate("/cluster/permissions/project-roles/configure", { state: { isUpdate: false, profile: undefined }})
          },
        }}
        secondaryActionsDisabled={!this.isSelected()}
        secondaryActions={[
          {
            id: "edit-profile",
            text: "Edit",
            onClick: () => {
              // Need to get role to retrieve permissions, since we don't get them on this page
              this.authzClient().getRole({
                role_id: this.getSelectedPermissionProfile()!.role_id
              }).then((response) => {
                this.props.navigate("/cluster/permissions/project-roles/configure", { 
                  state: {
                    isUpdate: true,
                    profile: response.role,
                    fromPage: 'list',
                  }
                });
              });
            },
          },
          {
            id: "delete-profile",
            text: "Delete",
            onClick: () => {
              const numAffectedProjects = this.state.affectedProjects.get(this.state.selectedPermissionProfile[0].role_id) ?? 0;
              if (numAffectedProjects === 0) {
                this.deleteProfile();
                return;
              }
              this.setFlashbarMessage(
                "error",
                "Your request could not be processed because users or groups are still associated with that role. Check the affected projects, remove the users/groups, or change the role assignments.",
                `Failed to delete ${this.state.selectedPermissionProfile[0].name} role`,
                <Button
                  variant="normal"
                  iconName="external"
                  iconAlign="right"
                  onClick={() => {
                    this.props.navigate(`/cluster/permissions/project-roles/${this.state.selectedPermissionProfile[0].role_id}`, { state: {
                      activeTabId: "affected-projects"
                    }});
                  }}
                >View affected projects</Button>
              );
            },
          },
        ]}
        showPaginator={true}
        showFilters={true}
        filters={[
          {
              key: "role_id",
          },
        ]}
        filteringPlaceholder="Find role by ID"
        onFilter={(filters) => {
          const token = `${filters[0].value ?? ""}`.trim();
          if (token.trim().length === 0) {
              return [];
          } else {
              return [
                  {
                      key: "role_id",
                      like: token,
                  },
              ];
          }
      }}
        onRefresh={() => {
          this.setState(
            {
              profileSelected: false,
            },
            () => {
              this.getListing().fetchRecords();
            }
          );
        }}
        selectedItems={this.state.selectedPermissionProfile}
        onSelectionChange={(event) => {
          this.setState({
            profileSelected: true,
            selectedPermissionProfile: event.detail.selectedItems
          })
        }}
        onFetchRecords={async () => {
          const response = await this.authzClient().listRoles({
            filters: this.getListing().getFilters(),
            paginator: this.getListing().getPaginator(),
          });
          this.setState({
            affectedProjects: (await Utils.getAffectedProjects(this.projectsClient(), this.authzClient())).affectedProjects,
            roleCount: response.items.length ?? 0
          });
          return {
            listing: response.items,
            paginator: response.paginator,
          }
        }}
        columnDefinitions={this.PERMISSION_PROFILES_TABLE_COLUMN_DEFINITIONS}
      />
    );
  }

  render() {
    return (
        <React.Fragment>
            {this.buildListing()}
        </React.Fragment>
    );
}
}

export default withRouter(PermissionProfilesDashboard);