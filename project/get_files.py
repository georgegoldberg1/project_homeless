def get_files(loc='.', ext:str=None, include_subdir:bool=True, ignore_hidden:bool=True):
    """Returns matching files in a specified directory and subfolders. 

    Defaults to recursive search of working directory, but match_path arg can be changed to customise search pattern.
        
    Args:
        loc (str): top directory for search = '.'
        ext (str, optional): file extension filter = None
        include_subdir (bool, optional): Whether to include filepaths in subdirectories = True
        ignore_hidden (bool, optional): Whether to exclude files starting with a period eg '.DS_Store', '.env' = True
    
    Returns:
        list: The list of paths found matching your query
        
    Note: 
        Uses pathlib module. `from pathlib import Path`
        
    """     
    if include_subdir:
        match_path = '**/*'
    else:
        match_path = '*'
    
    if ext:
        match_path = match_path + ext
    
    # search path + filter for extensions
    from pathlib import Path
    p = Path(loc).glob(match_path)
    
    # filter to remove .env/.DS_Store and other hidden files/folders
    if ignore_hidden:
        files = [x for x in p if x.is_file() and all([
            True if y[0] != '.' else False for y in x.parts
        ])]
    else:
        files = [x for x in p if x.is_file()]
    
    return files