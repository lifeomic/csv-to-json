# Accepted Transformations

Note that the order for transform types is file transformations then column transformations and finally JSON structure transformations. Within each transform list, transformations of the same category are performed in the order they are listed in the mapping file.

## File Transformations

These transformations apply to the entire supplied .csv file and occur before any other transformations. Note that these transforms must be placed as the first item in the JSON in a list under the name 'file-transforms'.

- transpose: Switches rows and columns of the inputted .csv file
- dictionary-from-file: Creates a dictionary (set of key-value pairs) from an additional **inputFile** that can be used for certain transformations (see fill-from-dictionary generation transform); a **dictionaryName**, **keyCol**, and **valueCol** must also be provided; **separation** is optional and defaults to ',' for comma-separated values

## Column Transformations

These transformations apply to a specific column in the supplied .csv file. They occur after file transformations but before JSON structure transformations. These transformations are more efficient than JSON structure transformations. Because of this, anything that could be implemented as either a column transformation or JSON structure transformations should be implemented as column transformations.

- trim-whitespace: Trims whitespace at the beginning and end of all cells in the **sourceCol** (1)
- uppercase: Capitalizes all characters in all cells in the **sourceCol** (1)
- lowercase: Convert all characters in all cells in the **sourceCol** to lowercase (1)
- string-replacement: Convert all instances of the **stringToReplace** with **replacementString** in all cells in the **sourceCol** (1)
- substring: Slices a string from the **startIndex** to the **endIndex**; only one field is required (1)
- default: Changes all empty cells in the **sourceCol** to the provided **defaultValue** (1)
- string-concatenation: Adds the **beforeString** before any text in the **sourceCol** and the **afterString** after any text in the **sourceCol** (1)
- format-date: Formats the date found in all cells in the **sourceCol** according to iso8601 (1)
- time-delta: Adds the supplied **days**, and **hours** to the supplied **baseCol**; columns or fixed values are accepted for any of the fields; only one field other than **baseCol** is required (2)

(1): **sourceCol** required

(2): **sourceCol** not accepted

## JSON Structure Transformations

- fill-from-dictionary: Fills in values from a dictionary that was created with the dictionary-from-file file transform; **dictionaryName** must be provided along with a **key** for the value that should be accessed from the dictionary; **key** can be a fixed or column value

### Conditionals

Conditionals are a more advanced type of generation transform that perform a conditional check on the given values. Note that **empty** and **occupied** are accepted as **compareTo** values with the **eq** **condition**. **empty** returns true if the given cell is empty and false otherwise. **occupied** returns true if the given cell is occupied and false otherwise.

- conditional: Compares the **sourceCol** to the **compareTo** based on the **condition**; a **values** object must be provided in the transform with a **true** value and a **false** value; **true** and **false** can be fixed or column values
- deletion-conditional: Compares the **sourceCol** to the **compareTo** based on the **condition**; if the condition evaluates to false, the object the transformation applies to and all sub-objects are not included in the output; if the condition evaluates to true, the object the transformation applies to will be included in the output; if multiple deletion-conditions are included, they are automatically ANDED together, meaning all deletion-conditionals present must evaluate to true for the object to be included in the output

#### Acceptable Conditional Comparisons

- eq
- less-than
- greater-than
- less-than-or-equal-to
- greater-than-or-equal-to
- not-eq
- not-less-than
- not-greater-than
- not-less-than-or-equal-to
- not-greater-than-or-equal-to
