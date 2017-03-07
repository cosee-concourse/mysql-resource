# MySQL User/Database Managment Resource

Creates/removes user or databases and handles DB/TABLE rights specified in a yaml. 

## Source Configuration

* `user`: *Required.* Username used as login

* `password`: *Required.* Password used as login.

* `host`: *Required.* Hostname of MySQL server.

## Behavior

### `check`: Checks configuration

Checks login credentials and tests connection to MySQL server

### `in`: Noop

#### Parameters

*None.*

### `out`: Executes SQL commands 

Executes SQL commands read from a sql file

#### Parameters
 
* `config_file`: *Required* File path to configuration yaml file.

Configuration is in following format:
``` yaml
commands:
    - ...
```
Example:
``` yaml
commands:
    - ...
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

```
- put: mysql
  params: 
     config_file: source/script.sql
```
