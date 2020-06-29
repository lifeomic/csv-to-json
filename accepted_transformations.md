# Accepted Transformations
## File Transformations
These transformations apply to the entire supplied .csv file and occur before any other transformations.
 - transpose: Switches rows and columns of the inputted .csv file
 ## Column Transformations
These transformations apply to a specific column in the supplied .csv file. They occur after file transformations but before JSON structure transformations. These transformations are more efficient than JSON structure transformations. Because of this, anything that could be implemented as either a column transformation or JSON structure transformations should be implemented as column transformations.
 - trim-whitespace: Trims whitespace at the beginning and end of all cells in the **sourceCol** (1)
 - uppercase: Capitalizes all characters in all cells in the **sourceCol** (1)
 - lowercase: Convert all characters in all cells in the **sourceCol** to lowercase (1)
 - string-replacement: Convert all instances of the **stringToReplace** with **replacementString** in all cells in the **sourceCol** (1)
 - substring: **NEED TO DO THIS**
 - default: Changes all empty cells in the column to the provided **defaultValue**; if the **sourceCol** is not provided, a column with all cells containing the **defaultValue** is created
 - string-concatenation: Adds the **beforeString** before any text in the **sourceCol** and the **afterString** after any text in the **sourceCol** (1)
 - format-date: Formats the date found in all cells in the **sourceCol** according to iso8601 (1)
 - time-delta: Adds the supplied **days**, and **hours** to the supplied **baseCol**; columns or fixed values are accepted for any of the fields; only one field other than **baseCol** is required (2)
 ## JSON Structure Transformations
- conditional: Compares the **sourceCol** to the **compareTo** based on the **comparison**; if the condition evaluates to false, the object the transformation applies to and all subobjects are not included in the output; if the condition evaluates to true, the object the transformation applies to will be included in the output; if multiple conditions are included, they are ANDED together
### Acceptable Conditional Comparisons:
- 

(1): **sourceCol** required

(2): **sourceCol** not accepted
