import gspread

if __name__ == '__main__':
    # TODO 20210814
    # default account path '/Users/yen/.config/gspread/service_account.json'
    gc = gspread.service_account()
    # Open a sheet from a spreadsheet in one go
    wks = gc.open_by_url('https://docs.google.com/spreadsheets/d/1vUnnfmRUeuBj44XXU-SJ8I3SPyOttMmyFSwDs1kaPdY/edit#gid=0').sheet1
    # Update a range of cells using the top left corner address
    wks.update('A1', [[1, 2], [3, 4]])
    # Or update a single cell
    wks.update('B42', "it's down there somewhere, let me take another look.")
    # Format the header
    wks.format('A1:B1', {'textFormat': {'bold': True}})