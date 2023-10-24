import datetime

def handleSalesFile(sales):
    sales.columns = sales.iloc[2]
    sales = sales.drop([0, 1, 2, 3])
    sales = sales.dropna(how='all')
    qty_loc = 20
    # if(month_names[i] == 'SALES_MAY.xls'):
    #     qty_loc = 19
    sales = sales.iloc[:, [0, 2, 16, qty_loc,28, 32, 35, 39]]
    sales.columns.values[3] = 'QTY'
    sales.columns.values[4] = 'JUMLAH'
    sales.columns.values[5] = 'HARGA POKOK'
    sales = sales.dropna()
    sales = sales.astype({"KODE": int, "NAMA STOCK": str, "QTY": int, "SUPPLIER": str, 
    "JUMLAH": float, "HARGA POKOK": float,"LABA": float, "%": float})
    return sales

def handleMasterFile(master_df):
    master_df.columns = master_df.iloc[2]
    master_df = master_df.drop([0, 1, 2, 3])
    master_df = master_df.iloc[:, [0, 2, 13, 21]]
    master_df.columns.values[2] = 'BS'
    master_df = master_df.dropna()
    master_df = master_df[master_df['KODE'] != 'KODE']
    master_df = master_df.astype({"KODE": int, "NAMA STOCK": str, "TOTAL": int})
    master_df.reset_index(drop=True, inplace=True)
    return master_df

def sort_by_date(string):
    month = string.split(' ')[0]
    year = string.split(' ')[1]
    # Convert the month and year to integers.
    month_int = datetime.datetime.strptime(month, '%B').month
    year_int = int(year)

    # Create a datetime object from the month and year integers.
    date = datetime.datetime(year_int, month_int, 1)

    return date

def handleMasterSupplier(supp_df):
    supp_df = supp_df.drop([0, 1, 2, 3])
    supp_df = supp_df.iloc[:, [0, 2, 10, 13, 18, 24]]
    supp_df.columns = ['KODE', 'NAMA STOCK', 'LAPANGAN', 'BS', 'GUDANG', 'TOTAL']
    supp_df = supp_df[supp_df['NAMA STOCK'] != 'NAMA STOCK']
    supp_df = supp_df.dropna(how='all')
    supp_df['index'] = supp_df.index
    
    stock_df = supp_df[supp_df['NAMA STOCK'].notna()]
    stock_df.reset_index(drop=True, inplace=True)

    supp_list_df = supp_df[supp_df['NAMA STOCK'].isna()]
    removeDate = supp_list_df['KODE'].str.contains('/') == False
    supp_list_df = supp_list_df[removeDate]
    supp_list_df.reset_index(drop=True, inplace=True)
    # supp_list_df['KODE'].replace('None', 'No Supp', inplace=True)
    
    list_supplier = []
    idx_supp = 0
    curr_supp = 0
    next_supp = 0
    for i in range(len(stock_df)):
        idx_item = stock_df['index'][i]
        if(idx_supp != len(supp_list_df)):
            curr_supp = supp_list_df['index'][idx_supp]
            next_supp = supp_list_df['index'][idx_supp+1] if (idx_supp < len(supp_list_df) - 1) else curr_supp
        if(idx_item > next_supp and idx_supp < len(supp_list_df)-1):
            idx_supp += 1
        supplier_name = 'No Supp' if (curr_supp > idx_item) else supp_list_df['KODE'][idx_supp]
        list_supplier.append(supplier_name)
    
    stock_df = stock_df.assign(Supplier=list_supplier)
    return stock_df