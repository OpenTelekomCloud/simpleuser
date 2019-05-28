import openstack
import logging


ROLE_MAPPING = {
    'ECS Admin': 'system_all_0',
    'ECS User': 'system_all_1',
    'ECS Viewer': 'system_all_2',
    'EVS Admin': 'system_all_4',
    'EVS Viewer': 'system_all_3',
    'VPC Admin': 'system_all_5',
    'VPC Viewer': 'system_all_6',
    'IMS Administrator': 'ims_adm'
}


def create_project(conn, name, description, parent_id, fake=False):
    project = conn.identity.find_project(name)
    if not project:
        if not fake:
            project = conn.identity.create_project(
                parent_id=parent_id,
                name=name,
                description=description)
    else:
        # Do nothing
        logging.info('Project %s exists already', name)
    return project

def create_group(conn, name, description, domain_id, fake=False):
    group = conn.identity.find_group(name)
    if not group:
        if not fake:
            group = conn.identity.create_group(
                name=name,
                description=description,
                domain_id=domain_id
            )
        else:
            logging.info('Group %s exists already', name)
    return group


def create_users(conn, group, users, fake=False):
    existing_users = get_group_users(conn, group)
    users_map = {u['name']: u for u in users}
    existing_users_map = {u['name']: u for u in existing_users}
    logging.debug(users_map)
    for user in users:
        if not user['name'] in existing_users_map:
            new_user = create_user(
                conn=conn,
                user=user,
                fake=fake)
            if new_user:
                conn.add_user_to_group(
                    new_user.id,
                    group
                )

    return existing_users


def create_user(conn, user, fake=False):
    if not fake:
        logging.info('Creating user %s', user['name'])
        user_args = {
            'name': user['name']
        }
        if 'email' in user:
            user_args['email'] = user['email']
        if 'description' in user:
            user_args['description'] = user['description']
        if 'mobile' in user:
            user_args['mobile'] = user['mobile']
        if 'password' in user:
            user_args['password'] = user['password']
        user = conn.identity.create_user(
            **dict(user_args)
        )
        return user
    else:
        logging.info('No user created')


def get_group_users(conn, group):
    """List users in the group

    This function is not present in any way in OpenStackSDK
    """
    users = []

    data = conn._identity_client.get(
        '/groups/{group}/users'.format(group=group))
    for user in data['users']:
        # Do we want to convert to proper User object?
        users.append(user)
    return users


def assign_roles_to_group(conn, group, project, roles, fake=False):
    if not fake:
        for role in roles:
            role_obj = conn.identity.find_role(role)
            conn.identity.assign_project_role_to_group(
                project=project,
                group=group,
                role=role_obj.id
            )
    else:
        logging.debug('Not assigning roles to group')


def create_resources(
    conn, fake, project_name, project_description,
    group_name, group_description, role_list, user_list
):
    """Main function to create all requested resources
    """
    root_project = conn.identity.find_project('eu-de')
    project = create_project(
        conn=conn,
        parent_id=root_project.id,
        name=project_name,
        description=project_description,
        fake=fake)

    logging.debug('project = %s' % project)

    domain_id = project.domain_id

    group = create_group(
        conn=conn,
        name=group_name,
        description=group_description,
        domain_id=domain_id,
        fake=fake
    )

    current_roles = conn.identity.role_assignments_filter(
        group=group.id,
        project=project.id)

    assign_roles_to_group(
        conn=conn,
        group=group.id,
        project=project.id,
        roles=role_list,
        fake=fake
    )

    # logging.debug(domain_id)
    # logging.debug(group)
    for role in current_roles:
        logging.debug(role)
        logging.debug(conn.identity.get_role(role.id))

    users = create_users(
        conn=conn,
        group=group.id,
        users=user_list,
        fake=fake
    )

    for user in users:
        logging.debug(user)


def main():

    logging.basicConfig(level=logging.DEBUG)
    openstack.enable_logging(debug=True, http_debug=True)
    # region = openstack.config.get_cloud_region('otc_demo_domain')
    # conn = openstack.connection.Connection(config=region)
    conn = openstack.connect()
    project_name = 'eu-de_test'
    project_descr = 'Test Project'
    group_name= 'test_group'
    group_descr = 'Test group'
    roles = [
        'server_adm',
        'te_admin'
    ]
    users = [
        {'name': 'test_user', 'description': 'some test user', 'mobile': '',
         'password': 'some_generated_stuff'}
    ]
    create_resources(
        conn=conn,
        fake=False,
        project_name=project_name,
        project_description=project_descr,
        group_name=group_name,
        group_description=group_descr,
        role_list=roles,
        user_list=users)


if __name__== "__main__":
  main()
