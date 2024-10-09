# WES - WRC RO-Crate

This document aims to detail a conversion between the [GA4GH WES profile](https://ga4gh.github.io/workflow-execution-service-schemas/docs/) to the [Workflow Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/) (WRC) extension of [Ro-Crates](https://www.researchobject.org/ro-crate/)

## WORKFLOW RUN CRATE RO-CRATE FIELDS

For a Json object to conform with the Ro-Crate specification there are certain minimal requirements. Further still the WRC estension has it's own requirements. Considering that, the following definitions aim to differentiate the diffrent types of fields and how they should be considered in each implementation.

### Terminology

1. constant: These fields are required and for our purposes the value of this field should always be the default value. In other words their values are constant.
2. required: These fields are required but their values are not constant.
3. recommended: These fields are not required but they are recommended to give a comprehensive definition for your RO-crate object.
4. optional: These fields are optional.

### `base object`

This is the base Ro-Crate object.

- **@context**(constant):
  - **WES field**: N/A
  - **type**: `string` | `[string]`
  - **description**: URI pointing to the official context page of the version of Ro-Crate and any extensions being implemented.
  - **default**:
  ```json
  [
    "https://w3id.org/ro/crate/1.1/context",
    "https://w3id.org/ro/terms/workflow-run/context"
  ]
  ```

### `metadata entity`

This entity is the metadata file descriptor. A Contextual Entity of type [CreativeWork](http://schema.org/CreativeWork), which describes the RO-Crate Metadata File and links it to the Root Data Entity.

reference: [https://www.researchobject.org/ro-crate/specification/1.1/metadata.html](https://www.researchobject.org/ro-crate/specification/1.1/metadata.html)

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: identifier for the metadata object and reference to the metadata file if one exists.
  - **default**:

  ```json
  "ro-crate-metadata.json"
  ```

- **@type**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type of the content stored in the Ro-Crate.
  - **default**:

  ```json
  "CreativeWork"
  ```

  - **conformsTo**(constant):

  * **WES field**: N/A
  * **type**: `{"@id": string}` | `[{"@id": string}]`
  * **description**: contains an `@id` field which is a URI pointing to the official specification page of the version of RoCrate and extensions implemented.
  * **default**:

  ```json
  [
    { "@id": "https://w3id.org/ro/crate/1.1" },
    { "@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0" }
  ]
  ```

- **about**(constant):

  - **WES field**: N/A
  - **type**: `{"@id": string}`
  - **description**: contains an `@id` field pointing to the dataset entity of the RO-Crate. Must match the dataset.@id field.
  - **default**:

  ```json
  { "@id": "./" }
  ```

### `Root data entity`

A Data Entity of type [Dataset](http://schema.org/Dataset), representing the Ro-Crate as a whole.

reference:

1. [https://www.researchobject.org/ro-crate/specification/1.1/metadata.html](https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html)
2. https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: identifier for the dataset object. Must match the metadata.@id feild
  - **default**:

  ```json
  "./"
  ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: a type for the dataset entity.
  - **default**:

  ```json
  "Dataset"
  ```

- **datePublished**(required):

  - **WES field**: N/A
  - **type**: [`Date`](https://schema.org/Date) | [`DateTime`](https://schema.org/DateTime)
  - **description**: The date the Ro-Crate was published. Must be a string in ISO 8601 date format and Should be specified to at least the precision of a day, May be a timestamp down to the millisecond.

- **name**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: Should identify the dataset to humans well enough to disambiguate it from other RO-Crates.
  - **default**:

  ```json
  "A Ga4GH WES Ro-Crate"
  ```

- **description**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: Should further elaborate on the name to provide a summary of the context in which the dataset is important.
  - **default**:
    ```json
    "A Wes Execution Service Ro-crate that conforms to the GA4GH WES specification"
    ```

- **mainEntity**(required):

  - **WES field**: N/A
  - **type**: `{"@id": "string"}`
  - **description**: Contains an `@id` field that points to a data entity, which contains the core data of the workflow log.
  - **default**:
    ```json
    "A Wes Execution Service Ro-crate that conforms to the GA4GH WES specification"
    ```

- **license**(required):
  - **WES field**: N/A
  - **type**: `{"@id": "string"}`
  - **description**: Contains an `@id` field that points to a contextual entity, which contains relevant information on the license for the Ro-crate data.
    SHOULD link to a Contextual Entity in the RO-Crate Metadata File with a name and description. MAY have a URI (eg for Creative Commons or Open Source licenses). MAY, if necessary be a textual description of how the RO-Crate may be used.

### `license object`

A contextual entity that contains relevant license information about the Ro-Crate.

reference: [https://www.researchobject.org/ro-crate/specification/1.1/metadata.html](https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html)

- **@id**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: A reference to a relevant and comprehensive description of the license. May be a URI to the official webpage describing the license.

- **@type**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type of the content stored in the Ro-Crate. Should match the `metadata.@type` field.

- **name**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The official name of the license.

- **description**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: Some additional context. May just be some standard license text. For example:
    ```
    "This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Australia License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/au/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."
    ```

- **identifier**(recommended):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: A reference to a relevant and comprehensive description of the license. May be a URI to the official webpage describing the license. Should match the `license.@id` field. Should be added as some algorithms may look for this instead.

### `mainEntity data Entity`

This object will contain or point to all relevant data for the GA4GH WES Run Log. This required by the WRC extension.

reference: https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/

- **id**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: a File URI linking to the workflow entry-point.

- **type**(constant):
  - **WES field**: N/A
  - **type**: `string` | `[string]`
  - **description**: The standard workflow type according to the Ro-Crate Version.
  - **default**:
    ```json
    ["File", "SoftwareSourceCode", "ComputationalWorkflow"]
    ```
- **name**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: A human-readable name for the workflow.

- **author**(recommended):

  - **WES field**: N/A
  - **type**: `{"@id": string}` | `[{"@id": string}]`
  - **description**: contains an `@id` field that points to the workflow author. Should point to a contextual entity with the author's information.

- **creator**(required):

  - **WES field**: N/A
  - **type**: `{"@id": string}` | `[{"@id": string}]`
  - **description**: contains an `@id` field that points to the workflow creator. Should point to a contextual entity with the creator's information.

- **identifier**(required):

  - **WES field**: `run_id` (one - one)
  - **type**: `string`
  - **description**: The Workflow run_id.

- **dateCreated**(required):

  - **WES field**: `run_log.start_time` (one - one)
  - **type**: [`Date`](https://schema.org/Date) | [`DateTime`](https://schema.org/DateTime)
  - **description**: The date the workflow started executing.

- **programmingLanguage**(required):

  - **WES field**: `request.workflow_type`
  - **type**: `{"@id": string}` (one - one)
  - **description**: contains an `@id` field, an IRI that points to official documentation for the prrogramming language the workflow was written in. Should match the `@id` field of a contextual entity with the workflow's programming language.

- **creativeWorkStatus**(required):

  - **WES field**: `state`
  - **type**: `UNKNOWN` | `QUEUED` | `INITIALIZING` | `RUNNING` | `PAUSED` | `COMPLETE` | `EXECUTOR_ERROR` | `SYSTEM_ERROR` | `CANCELED` | `CANCELING` | `PREEMPTED` (one - one)
  - **description**: The status of the workflow.

- **url**(required):

  - **WES field**: `request.workflow_url` (one - one)
  - **type**: `URL`
  - **description**: The workflow url.

- **keywords**(recommended):

  - **WES field**: `request.tags` (one - many)
  - **type**: `string`
  - **description**: The workflow keywords or tags. If there are multiple tags they should be delimited by commas.

- **runtimePlatform**(recommended):

  - **WES field**: `request.workflow_engine` (one - one)
  - **type**: `string`
  - **description**: The workflow engine.

- **softwareRequirements**(recommended):

  - **WES field**: `request.workflow_engine_parameters` (many - many)
  - **type**: `{"@id": string}` | `[{"@id": string}]`
  - **description**: The workflow engine parameters.

### `run_log entity` (optional)

This is one of the output objects that the mainEntity will point to. It is a data entity of type FormalParameter.

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The name of the WES run_log object.
  - **default**:
    ```json
    "#run_log"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the run_log entitiy.
  - **default**:
    ```json
    "FormalParameter"
    ```

- **name**(optional):

  - **WES field**: run_log.name
  - **type**: `string`
  - **description**: The task or workflow name.

- **dateCreated**(optional):

  - **WES field**: run_log.start_time
  - **type**: [`Date`](https://schema.org/Date) | [`DateTime`](https://schema.org/DateTime)
  - **description**: When the command started executing.

- **dateModified**(optional):

  - **WES field**: run_log.end_time
  - **type**: [`Date`](https://schema.org/Date) | [`DateTime`](https://schema.org/DateTime)
  - **description**: When the command stopped executing.

### `run_log.stdout entity` (optional)

one of the output objects of the main entity

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The name of the WES run_log.stdout string.
  - **default**:
    ```json
    "#run_log_stdout"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "FormalParameter"
    ```

- **name**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: name of the entity.
  - - **default**:
    ```json
    "Runlog stdout"
    ```

- **url**(required):

  - **WES field**: `run_log.stdout` (one - one)
  - **type**: `URL`
  - **description**: A URL to retrieve standard output logs of the workflow run or task.

### `run_log.stderr entity` (optional)

one of the output objects of the main entity

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The name of the WES run_log.stderr string.
  - **default**:
    ```json
    "#run_log_stderr"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "FormalParameter"
    ```

- **name**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: name of the entity.
  - - **default**:
    ```json
    "Runlog stderr"
    ```

- **url**(required):

  - **WES field**: `run_log.stderr` (one - one)
  - **type**: `URL`
  - **description**: A URL to retrieve standard error logs of the workflow run or task.

- ### `request.workflow_params.inputFile` | `request.workflow_params.inputDir` | `request.workflow_params.input` (optional)

one of the input objects of the main entity.

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The id of the WES request.input string.
  - **default**:
    ```json
    "#request_workflow_params_input"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "FormalParameter"
    ```

- **name**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: name of the entity.
  - - **default**:
    ```json
    "Request workflow_params input"
    ```

- **url**(required):

  - **WES field**: `request.workflow_params.inputFile` | `request.workflow_params.inputDir` | `request.workflow_params.input` (one - one)
  - **type**: `URL`
  - **description**: A URL to retrieve input data of the workflow run or task.

### `request.workflow_engine_parameters`(optional)

A data entity representing the `request.workflow_engine_parameters` field from the WES profile

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The name of the WES request.workflow_engine_parameter.
  - **default**:
    ```json
    "#request_workflow_engine_parameters"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "SoftwareApplication"
    ```

- **name**(required):

  - **WES field**: `request.workflow_engine_parameters[i]`
  - **type**: `string`
  - **description**: name of the parameter.

- **url**(required):

  - **WES field**: N/A
  - **type**: `URL`
  - **description**: A URL to the parameter.

### `request.workflow_type`(optional)

This entity is pointed to by the programmingLanguage property in the mainEntity data entity. It is a data entity of type `[ComputerLanguage](https://schema.org/ComputerLanguage)`.

- **@id**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The id of the progamming language field that points to this entity. Can be the URL of the official documentation of said programming language.

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "ComputerLanguage"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "ComputerLanguage"
    ```

- **name**(required):

  - **WES field**: `request.workflow_type`
  - **type**: `string`
  - **description**: name of the workflow type.

- **alternateName**(required):

  - **WES field**: `request.workflow_type`-`request.workflow_type_version`
  - **type**: `string`
  - **description**: name of the workflow type and the workflow type version, seperated by a hypen.

- **url**(required):

  - **WES field**: `request.workflow_engine_parameters`
  - **type**: `URL`
  - **description**: A URL to the workflow type. Usually the URL of the official documentation for the workflow type.

### `task_logs_url`

- **@id**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The id of the WES task_logs_url.
  - **default**:
    ```json
    "#task_logs_url"
    ```

- **@type**(constant):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type the entitiy.
  - **default**:
    ```json
    "FormalParameter"
    ```

- **name**(required):

  - **WES field**: N/A
  - **type**: `string`
  - **description**: name of the entity.
  - - **default**:
    ```json
    "The workflow Task Logs URL"
    ```

- **url**(required):

  - **WES field**: `task_logs_url` (one - one)
  - **type**: `URL`
  - **description**: A reference to the complete url which may be used to obtain a paginated list of task logs for this workflow.

one of the input objects of the main entity. A data entity representing the WES `task_logs_url`

### WES fields that have not been added:

1. outputs
2. run_log.cmd
3. run_log.exit_code
4. run_log.system_logs
5. request.workflow_params (partial support)
6. workflow_engine_version
7. task_logs (deprecated, may not be added)
