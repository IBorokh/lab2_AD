from spyre import server
import pandas as pd

server.include_df_index = True


class StockExample(server.App):
    title = "AD lab2 by Ivan Borokh"

    inputs = [{
        "type": 'dropdown',
        "id": "index",
        "key": "index",
        "label": 'Choose index',
        "options": [
            {"label": "VCI", "value": "VCI"},
            {"label": "TCI", "value": "TCI"},
            {"label": "VHI", "value": "VHI"}],
        "value": 'VHI',
        "action_id": "update_data"
    },

        {
            "type": 'dropdown',
            "id": "file",
            "key": "file",
            "label": 'Choose region',
            "options": [
                {"label": "1 Vinnytsia", "value": "1"},
                {"label": "2 Volyn", "value": "2"},
                {"label": "3 Dnipropetrovsk", "value": "3"},
                {"label": "4 Donetsk", "value": "4"},
                {"label": "5 Zhytomyr", "value": "5"},
                {"label": "6 Zakarpattya", "value": "6"},
                {"label": "7 Zaporizhzhya", "value": "7"},
                {"label": "8 Ivano-Frankivsk", "value": "8"},
                {"label": "9 Kyiv", "value": "9"},
                {"label": "10 Kirovohrad", "value": "10"},
                {"label": "11 Luhansk", "value": "11"},
                {"label": "12 Lviv", "value": "12"},
                {"label": "13 Mykolaiv", "value": "13"},
                {"label": "14 Odesa", "value": "14"},
                {"label": "15 Poltava", "value": "15"},
                {"label": "16 Rivne", "value": "16"},
                {"label": "17 Sumy", "value": "17"},
                {"label": "18 Ternopil", "value": "18"},
                {"label": "19 Kharkiv", "value": "19"},
                {"label": "20 Kherson", "value": "20"},
                {"label": "21 Khmelnytsky", "value": "21"},
                {"label": "22 Cherkasy", "value": "22"},
                {"label": "23 Chernivtsi", "value": "23"},
                {"label": "24 Chernihiv", "value": "24"},
                {"label": "25 Republic of Crimea", "value": "25"}],
            "value": '1',
            "action_id": "update_data"
        }]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "get statistics"
    }]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"},
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
        file_index = params['file']
        file = f"vhi_id_{file_index}_2020-05-23.csv"
        df = pd.read_csv(file, names=headers, header=1, index_col=False)
        data = pd.concat(df, ignore_index=True)
        data = data.drop(data.loc[data['VHI'] == -1].index)
        data = data.replace(to_replace='<tt><pre>', value='', regex=True)
        data = data.replace(to_replace='</pre></tt>', value='', regex=True)
        data = data.dropna()
        data = data.reset_index(drop=True)
        return data

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot()
        plt_obj.set_ylabel(f"{params['index']}")
        plt_obj.set_xlabel("Date")
        plt_obj.set_title(f"{params['index']} statistics")
        return plt_obj.get_figure()


app = StockExample()
app.launch(port=9093)
