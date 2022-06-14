# cloakit_api
Non official Python Api for https://cloakit.pro

![image](https://user-images.githubusercontent.com/97606234/173595209-fffc3d19-f520-47df-8e64-d7041c98ab3e.png)


```python
from cloak_it import CloakIT

cit = CloakIT()

# connect to service
info = cit.connect(email='',password='')
print(info) # print account info

# get company list
cl = cit.company_list()
print(cl)

# create new company
new_company = cit.create_company(name='test_company', 
              white_url='https://google.com', loadTypeWhite='redirect', 	
              offer_url='https://rambler.com', loadTypeOffer='load')
            
new_company_id = result['_id']

# switch company mode (active/pause)
ans = cit.switch_mode(company_id=new_company_id)
print(ans)

# get data for .php cloak file
file_data = cit.get_file(new_company_id)
print(file_data)

ans = cit.delete_company(new_company_id)
print(ans)
```
