## schema

### base object
* **@context(static)**:
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

### metadata object
reference: [https://www.researchobject.org/ro-crate/specification/1.1/metadata.html](https://www.researchobject.org/ro-crate/specification/1.1/metadata.html)

* **@id**(static):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: identifier for the metadata object and reference to the metadata file if one exists.
  - **default**:
  ```json
  "ro-crate-metadata.json"
  ```

  * **conformsTo**(static):
  - **WES field**: N/A
  - **type**: `{"@id": string}` | `[{"@id": string}]`
  - **description**: contains an `@id` field which is a URI pointing to the official specification page of the version of RoCrate and extensions implemented.
  - **default**:
  ```json
  [
    {"@id": "https://w3id.org/ro/crate/1.1"},
    {"@id": "https://w3id.org/workflowhub/workflow-ro-crate/1.0"}
  ]
  ```

* **about**(static):
  - **WES field**: N/A
  - **type**: `{"@id": string}`
  - **description**: contains an `@id` field pointing to the dataset entity of the RO-Crate. Must match the dataset.@id field.
  - **default**:
  ```json
   {"@id": "./"},
  ```

  * **about**(static):
  - **WES field**: N/A
  - **type**: `{"@id": string}`
  - **description**: contains an `@id` field pointing to the dataset entity of the RO-Crate. Must match the dataset.@id field.
  - **default**:
  ```json
   {"@id": "./"},
  ```
### dataset object
reference: 
1. [https://www.researchobject.org/ro-crate/specification/1.1/metadata.html](https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html)
2. https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/

* **@id**(static):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: identifier for the dataset object. Must match the metadata.@id feild
  - **default**:
  ```json
    "./"
  ```

* **@type**(static):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: a type for the dataset entity. 
  - **default**:
  ```json
    "Dataset"
  ```

 * **datePublished**(static):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: The date the Ro-Crate was published. Must be a string in ISO 8601 date format and Should be specified to at least the precision of a day, May be a timestamp down to the millisecond.

* **name**(static):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: Should identify the dataset to humans well enough to disambiguate it from other RO-Crates.
  - **default**:
  ```json
    "A Ga4GH WES Ro-Crate"
  ```

* **description**(static):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: Should further elaborate on the name to provide a summary of the context in which the dataset is important.
  - **default**:
    ```json
      "A Wes Execution Service Ro-crate that conforms to the GA4GH WES specification"
    ```

* **mainEntity**(required):
  - **WES field**: N/A
  - **type**: `{"@id": "string"}`
  - **description**: Contains an `@id` field that points to a data entity, which contains the core data of the workflow log. 
  - **default**:
    ```json
      "A Wes Execution Service Ro-crate that conforms to the GA4GH WES specification"
    ```
  
