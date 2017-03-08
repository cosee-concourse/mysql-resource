# MySQL User/Database Management Resource

Creates/removes user or databases and handles database user rights specified in a yaml. 

## Source Configuration

* `user`: *Required.* Username used as login

* `password`: *Required.* Password used as login.

* `host`: *Required.* Hostname of MySQL server.

## Behavior

### `check`: Checks and validates configuration

Checks login credentials and tests connection to MySQL server

### `in`: No-op

#### Parameters

*None.*

### `out`: Executes SQL operations.

Executes SQL operations specified in a yaml. Needs to be in a specific format (defined below).

#### Parameters
 
* `config_file`: *Required* File path to yaml configuration file.

Operations must be specified in the following format. All operations are optional.
``` yaml
DATABASES:
    CREATE: 
        # list of databases to create
        - DB1
        - DB2
    REMOVE: 
        # list of databases to remove
        - DB4
        - DB5
USERS:
    CREATE:
        # list of users to create
        - USERNAME: username
          PASSWORD: password        
        - USERNAME: username2
          PASSWORD: password2
    GRANT-ALL:
        # list of users to grant all rights on a database
        - USER: username
          DATABASE: database-name        
        - USER: username
          DATABASE: database-name
    GRANT-SELECT:
        # list of users to grant SELECT rights on a database
        - USER: username
          DATABASE: database-name
        - USER: username2
          DATABASE: database-name
    GRANT-SELECT-TABLE:
        # list of users to grant SELECT right on a specific table in a database
        - USER: username
          DATABASE: database-name
          TABLE: table-name        
        - USER: username2
          DATABASE: database-name
          TABLE: table-name
        
```

## Example Configuration

### Resource Type
``` yaml
- name: mysql-resource
  type: docker-image
  source:
    repository: quay.io/cosee-concourse/mysql-resource
```
### Resource

``` yaml
- name: mysql
  type: mysql-resource
  source:
    user: USER
    password: PASSWORD
    host: HOSTNAME
    port: PORT
```

### Plan

``` yaml
- put: mysql
  params: 
     config_file: source/script.sql
```
