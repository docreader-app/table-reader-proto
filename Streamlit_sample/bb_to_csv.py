import json
import pandas as pd

# with open('nanoresponse.json', 'r') as file:
#     data = json.load(file)

def convert_json_to_df(jsondata):
    print(jsondata)
    words_data = []
    for result in jsondata['results']:
        for page in result['page_data']:
            words = page['words']
            for word in words:
                words_data.append({
                    'text': word['text'],
                    'xmin': word['xmin'],
                    'ymin': word['ymin'],
                    'xmax': word['xmax'],
                    'ymax': word['ymax']
                })

    # Sort words by ymin first, then by xmin to arrange them in rows and columns
    words_data = sorted(words_data, key=lambda x: (x['ymin'], x['xmin']))

    def group_words_into_rows(words, y_threshold=10):
        rows = []
        current_row = []
        current_y = words[0]['ymin']
        
        for word in words:
            if abs(word['ymin'] - current_y) <= y_threshold:
                current_row.append(word)
            else:
                rows.append(current_row)
                current_row = [word]
                current_y = word['ymin']
        
        rows.append(current_row)
        return rows

    rows = group_words_into_rows(words_data)

    table_data = []
    for row in rows:
        row_data = [word['text'] for word in row]
        table_data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(table_data)

    # Save to CSV
    # df.to_csv('reconstructed_table.csv', index=False, header=False)

    # # Display the DataFrame
    # print(df.head())
    return df
