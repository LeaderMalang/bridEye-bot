import requests
import os
import csv
import tempfile
import shutil
from get_current_watchers import get_current_watchers
from jupiter_api.jupiter_api import create_order
import asyncio

#api key for brideye
brideye_key=os.environ.get("BRID_EYE_KEY")
#base url of public API endpoint
public_api_endpoint=os.environ.get("PUBLIC_API_ENDPOINT")
wallet_public_key=os.environ.get("PUBLIC_KEY")
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

def buy_token(from_wallat,to_wallat,value):
  pass
def check_decrease_percentage(token_address):
  pass


def calculate_percentage_increase(initial_value, updated_value):

    # Calculate the increase in value
  
  increase = updated_value - initial_value
    
    # Calculate the percentage increase
  
  if initial_value == 0:
        # Handle the case where the initial value is zero to avoid division by zero
    
    percentage_increase = float('inf')  # Infinite increase
  else:
    percentage_increase = (increase / initial_value) * 100
    
    # Return the percentage increase
  return percentage_increase

def calculate_percentage_decrease(initial_value, updated_value):
    # Calculate the decrease in value
  decrease = initial_value - updated_value
    
    # Calculate the percentage decrease
  if initial_value == 0:
        # Handle the case where the initial value is zero to avoid division by zero
    percentage_decrease = float('inf')  # Infinite decrease
  else:
    percentage_decrease = (decrease / initial_value) * 100
    
    # Return the percentage decrease
  return percentage_decrease


async def modify_price_in_csv(file_path):
  await asyncio.sleep(1)
  temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)

  with open(file_path, mode='r', newline='') as csv_file, temp_file:

    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(temp_file)
    line_count = 0
    for row in csv_reader:
      if len(row)==0:
        continue
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
       

        watchers_with_time_list=get_current_watchers(token_address)
        last_watchers_count=row[3]
        print(f"last watchers count, {last_watchers_count}")
        last_watchers_time=row[4]
        print(f"last watchers time, {last_watchers_time}")
        last_24h_view_count=row[5]
        print(f"last 24h view, {last_24h_view_count}")
        last_24h_view_perce=row[6]
        print(f"last 24h view percentage, {last_24h_view_perce}")
        if isinstance(watchers_with_time_list, list):

          row[3]=int(watchers_with_time_list[0])
          print(f"current watchers count, {watchers_with_time_list[0]}")
          row[4]=watchers_with_time_list[1]
          print(f"current watchers time, {watchers_with_time_list[1]}")
          row[5]=watchers_with_time_list[2]
          print(f"current 24h view count, {watchers_with_time_list[2]}")
          row[6]=watchers_with_time_list[3]
          print(f"current 24h view percentage, {watchers_with_time_list[3]}")
          perc_increase=0
          perc_decrease=0
          input_mint=os.environ.get("INPUT_MINT")
          if last_watchers_count is not None and last_watchers_count!= '':
            perc_increase=calculate_percentage_increase(int(last_watchers_count),int(watchers_with_time_list[0]))
            print(f" percentage increase in watchers count, {perc_increase}")
          if perc_increase>=10 and row[6]>=10.0:
            #place buy of 1 $ 
            amount=0.0070
            
            transaction_id=await create_order(input_mint,token_address,amount,'buy')
          
            print(f" buy response,{transaction_id}")
          
          if last_24h_view_count is not None and last_24h_view_count!= '':
            perc_decrease=calculate_percentage_decrease(int(last_24h_view_count), int(watchers_with_time_list[2]))
            print(f" percentage decrease in watchers count, {perc_decrease}")
          if perc_decrease <0 and row[6]<0.0:
            #place sell  
            transaction_id=await create_order(token_address,input_mint,0,'sell')
            print(f"sell response,{transaction_id}")
            #call buy function
        else:
          print("No watchers found")

      csv_writer.writerow(row)

    # Close the original file and the temporary file
    csv_file.close()
    temp_file.close()

    # Replace the original file with the temporary file
    # Replace the original file with the temporary file using a different approach
    shutil.copyfile(temp_file.name, file_path)  # Copy the temporary file to the original file path

    # Delete the temporary file
    os.unlink(temp_file.name)

async def run_main_every_minute(file_path):

  while True:
    print("Checking after 1 minute...")
        # Run the main function with the provided order_id
    await modify_price_in_csv(file_path)
        
        # Wait for one minute (60 seconds) before running the function again
    await asyncio.sleep(60)




if __name__ == "__main__":

 
  file_path = 'crypto_tokens.csv'  # Path to the CSV file
  asyncio.run(run_main_every_minute(file_path))
  # modify_price_in_csv(file_path)
  print("Job Completed")

  

