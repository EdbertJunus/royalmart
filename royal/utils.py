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