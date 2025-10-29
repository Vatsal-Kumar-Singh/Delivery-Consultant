from utils.data_processing import load_and_merge_data

if __name__ == '__main__':
    df = load_and_merge_data()
    print('Loaded df shape:', df.shape)
