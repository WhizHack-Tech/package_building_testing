import pandas as pd
import numpy as np
import gc, pickle
def feature_manipulation(data):
    data = data.copy()
    data_frame = data.copy()
    selected_columns = ['location','syscheck.mode','syscheck.gname_after','syscheck.changed_attributes','syscheck.event','decoder.name',
                        'data.title','data.alert_type','data.dstuser','data.srcip','data.srcport','data.audit.type',
                        'data.sca.type','data.sca.check.result','data.sca.check.reason','data.sca.total_checks','data.sca.score',
                        'data.dpkg_status','data.package','syscheck.size_before','syscheck.size_after','syscheck.inode_before',
                        'syscheck.inode_after','syscheck.perm_before','syscheck.perm_after','syscheck.path','data.file','data.pwd',
                        'data.sca.check.file','data.sca.check.directory','data.command','data.audit.command']
    for i in selected_columns:
        if i not in data.columns:
            data[i] = np.nan
    # This code simplifies the logic by grouping the columns that need to be filled with NaN values and the columns that need to be converted to integers.
    def sca_checkfile(data):
        columns_to_fillna = ['data.sca.check.file', 'data.sca.check.directory']
        data[columns_to_fillna[0]] = data[columns_to_fillna[0]].fillna(data[columns_to_fillna[1]])
        columns_to_convert_to_integer = ['syscheck.size_before', 'syscheck.size_after', 'syscheck.inode_before', 'syscheck.inode_after']
        for col in columns_to_convert_to_integer:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce', downcast='integer').fillna(0)
                
    sca_checkfile(data)
    # This function applies all the feature manipulation to data
    def Determine_sys_size(row):
        size_before = row["syscheck.size_before"]
        size_after = row["syscheck.size_after"]
        event = row["syscheck.event"]
        if size_before == 0 and size_after > 0:
            if event == "deleted":
                return "create"
            elif event == "added":
                return "upgrade"
        elif size_before != size_after and event == "modified":
            return "modified"
        else:
            return "no change"
    data['syscheck_size'] = data.apply(Determine_sys_size,axis=1)
    
    # This function combines path related features into one
    def Fill_path(data):
        data['file_path'] = np.nan
        for i in ['syscheck.path','data.file','data.pwd','data.sca.check.file']:
            if i in data.columns:
                data['file_path'] = data['file_path'].fillna(data[i])
            else:
                pass
    Fill_path(data)
        
    # This function combines command related features into one
    def Fill_command(data):
        data['command']  = np.nan
        if 'data.command' in data.columns:
            data['command'] = data['data.command']
        if 'data.audit.command' in data.columns:
            data['command'] = data['command'].fillna(data['data.audit.command'])
        # return df['command']
    Fill_command(data)
    # This function extracts command from command feature
    def Extract_command(path):
        if isinstance(path, str):
            parts = path.split('/')
            command = parts[-1] 
            return command
        else:
            return path
    data['command'] = data['command'].apply(Extract_command)
    def Compare_permissions(row):
        perm_before = row['syscheck.perm_before']
        perm_after = row['syscheck.perm_after']
        if pd.isna(perm_before) and not pd.isna(perm_after):
            return "Added"
        elif not pd.isna(perm_before) and pd.isna(perm_after):
            return "Removed"
        elif perm_before == perm_after:
            return "UnChanged"
        else:
            return "Changed"
    data['syscheck_perm'] = data.apply(Compare_permissions, axis=1)

    def Determine_inode(row):
        try:
            if row['syscheck.inode_before'] > row['syscheck.inode_after']:
                return "Deleted"
            elif row['syscheck.inode_before'] < row['syscheck.inode_after']:
                return "Modified"
            else:
                return "No change"
        except KeyError:
            pass
    
    data['syscheck_inode'] = data.apply(Determine_inode, axis=1)
    # This function converts features to numerics and imputes missing values 
    def Fill_missing_value_numeric_cols(data):
        for i in ['data.srcport','data.sca.total_checks','data.sca.score']:
            if i in data.columns:
                data[i] = data[i].fillna(0)
                data[i] = data[i].astype(int)
            else:
                pass
            
    Fill_missing_value_numeric_cols(data)
    # This function imputes missing values for categorical features
    def Fill_missing_value_categorical_cols(data):
        for i in [i for i in data.columns if 'syscheck' in i]:
            data[i].fillna('nosys',inplace=True)
        for i in [i for i in data.columns if 'sca' in i]:
            data[i].fillna('nosca',inplace=True)
        for i in ['data.title','data.alert_type','data.dstuser','data.srcip','data.audit.type','data.dpkg_status','data.package','file_path','command']:
            if i in data.columns:
                data[i].fillna('not found',inplace=True)
    Fill_missing_value_categorical_cols(data)
    
    model_lst = ['location', 'syscheck.mode',
       'syscheck.gname_after', 'syscheck.changed_attributes', 'syscheck.event',
       'decoder.name', 'data.title', 'data.alert_type', 'data.dstuser',
       'data.srcip', 'data.srcport', 'data.audit.type', 'data.sca.type',
       'data.sca.check.result', 'data.sca.check.reason',
       'data.sca.total_checks', 'data.sca.score', 'data.dpkg_status',
       'data.package','syscheck_size', 'syscheck_inode', 'syscheck_perm','file_path', 'command']

    # This function categorizes numerical and categorical columns
    def getNumericalAndCategorical(data):
        numeric_cols = [key for key in dict(data.dtypes) if dict(data.dtypes)[key] in ['float64', 'int64', 'float32', 'int32']]
        categorical_cols = [key for key in dict(data.dtypes) if dict(data.dtypes)[key] not in ['float64', 'int64', 'float32', 'int32']]
        return [numeric_cols, categorical_cols]

    # This function converts list to string
    def list2Str(lst):
        try:
            if isinstance(lst, list):
                return",".join(lst)
            else:
                return lst
        except:
            pass
    cat_cols = getNumericalAndCategorical(data[model_lst])[1]
    data[cat_cols] = data[cat_cols].applymap(lambda x:list2Str(x))
    
    model = pickle.load(open('linux_pickle1.pkl','rb'))
    data_frame['anomaly_label'] = model.predict(data[model_lst])
    # print('Values: ', data_frame['anomaly_label'].value_counts(dropna = False))
    data=data.add_suffix('_')
    append_str = '_'
    model_lst= [sub + append_str for sub in model_lst]
    dataframe =  pd.concat([data_frame, data[model_lst]], axis = 1)
    dataframe = dataframe.drop_duplicates(subset=model_lst)
    dataframe.drop(columns=model_lst, inplace=True)
    del data, model_lst, append_str, selected_columns
    gc.collect()
    return dataframe
