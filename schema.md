## schema

### WORKFLOW RUN CRATE RO-CRATE FIELDS

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

* **@type**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type of the content stored in the Ro-Crate. Should match the `license.@type` field if it exists.


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

* **license**(recommended):
  - **WES field**: N/A
  - **type**: `{"@id": "string"}`
  - **description**: Contains an `@id` field that points to a contextual entity, which contains relevant information on the license for the Ro-crate data.
    SHOULD link to a Contextual Entity in the RO-Crate Metadata File with a name and description. MAY have a URI (eg for Creative Commons or Open Source licenses). MAY, if necessary be a textual description of how the RO-Crate may be used.
 
### license object
A contextual entity that contains relevant license information about the Ro-Crate.

reference: [[https://www.researchobject.org/ro-crate/specification/1.1/metadata.html]](https://www.researchobject.org/ro-crate/specification/1.1/root-data-entity.html)

* **@id**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: A reference to a relevant and comprehensive description of the license. May be a URI to the official webpage describing the license.

* **@type**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: The type of the content stored in the Ro-Crate. Should match the `metadata.@type` field.
 
* **name**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: The official name of the license.
 
* **description**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: Some additional context. May just be some standard license text. For example:
    ```
    "This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Australia License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/au/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."
    ```

* **identifier**(recommended):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: A reference to a relevant and comprehensive description of the license. May be a URI to the official webpage describing the license. Should match the `license.@id` field. Should be added as some algorithms may look for this instead.

### mainEntity object
This object will contain or point to all relevant data for the GA4GH WES Run Log.

* **id**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**: a File URI linking to the workflow entry-point.

* **type**(static):
  - **WES field**: N/A
  - **type**: `string` | `[string]`
  - **description**:  The standard workflow type according to the Ro-Crate Version.
  - **default**:
    ```json
      ["File", "SoftwareSourceCode", "ComputationalWorkflow"]
    ```
    
* **name**(required):
  - **WES field**: N/A
  - **type**: `string`
  - **description**:  A human-readable name for the workflow.

* **author**(recommended):
  - **WES field**: N/A
  - **type**: `{"@id": string}`
  - **description**: contains an `@id` field that points to the workflow author. Should point to a contextual entity with the author's information.
 
* **creator**(recommended):
  - **WES field**: N/A
  - **type**: `{"@id": string}`
  - **description**: contains an `@id` field that points to the workflow creator. Should point to a contextual entity with the creator's information.
 
* **programmingLanguage**(recommended):
  - **WES field**: N/A
  - **type**: `{"@id": string}`
  - **description**: contains an `@id` field that points to the prrogramming language the workflow was written in. Should point to a contextual entity with the workflow's programming language.

### GA4GH WES FIELDS

* **indentifier**(required):
  - **WES field**: run_id
  - **type**: `string`
  - **description**: The Workflow run_id.
 

 



