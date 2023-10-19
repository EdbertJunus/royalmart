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