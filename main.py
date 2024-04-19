import requests
import os
import csv
import tempfile
import shutil


#api key for brideye
brideye_key=os.environ.get("BRID_EYE_KEY")
#base url of public API endpoint
public_api_endpoint=os.environ.get("PUBLIC_API_ENDPOINT")

#function to get token price of token from address 
def get_token_price(token_address):
  

  url = "{1}/defi/price?address={0}".format(token_address,public_api_endpoint)

  headers = {"X-API-KEY": brideye_key}
  result=None
  try:
  
    response = requests.get(url, headers=headers)
    result=response.json()
  except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")
    
  if result is not None and "success" in result and result["success"]==True:
    return result["data"]
  else :
    return result


def check_increase_decrease_percentage(token_address):
  pass







def modify_price_in_csv(file_path):

  temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)

  with open(file_path, mode='r', newline='') as csv_file, temp_file:

    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(temp_file)
    line_count = 0
    for row in csv_reader:

      if line_count == 0:

        print(f'Column names are {", ".join(row)}')
        line_count += 1
      else:
        print("Getting Token new Price ,",row[0])
        token_address=row[0]
        current_price=get_token_price(token_address)
        print("Current Token Price ,",current_price["value"])
        row[1]=current_price["value"]
        row[2]=current_price["updateHumanTime"]
        print("Updating Token Price ,",current_price["updateHumanTime"])
      csv_writer.writerow(row)

    # Close the original file and the temporary file
    csv_file.close()
    temp_file.close()

    # Replace the original file with the temporary file
    # Replace the original file with the temporary file using a different approach
    shutil.copyfile(temp_file.name, file_path)  # Copy the temporary file to the original file path

    # Delete the temporary file
    os.unlink(temp_file.name)






if __name__ == "__main__":

 
  file_path = 'crypto_tokens.csv'  # Path to the CSV file
  modify_price_in_csv(file_path)
  print("Job Completed")

  

