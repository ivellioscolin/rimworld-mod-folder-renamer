# Rimworld Mod folder Renamer

## Description
If using RimPy Mod Manager to manage and update all steam mods, the mod folder must have specific name equal to its steam workshop ID. However it makes the folder non-intuitive if not using RimPy.

The script automatically converts the mod folder bi-directional:  
* If using steam style, the folder will only remain its workship ID as "\<steam workshop ID\>".
* If using friendly name, the folder will be constructed as "\<steam workshop ID\>(\<mod name\>)".
* For non-steam mod, the folder will be renamed to "\<mod name\>".

To use the script, you need copy database/db.json from RimPy to the script folder.

## Usage
```python
python rmr.py <mod_dir> <mode> <t>
```
  
    mod_dir:
        The parent directory of all mods  
    mode:  
        s: steam style  
        n: friendly name  
    t:
        Trial run
