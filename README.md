# Pocket Sense 

## API ENDPOINTS  

Register user    

---
Endpoint - > localhost:8000/api/register  
Payload  
{  
    "username" : "kaushikaryan",  
    "password" : "aryan@1234",  
    "password2" : "aryan@1234",  
    "email" : "email@mail.com",  
    "first_name" : "aryan",  
    "last_name" : "kaushik"  
}  
---
Endpoint -> localhost:8000/api/login  
Payload  
{  
    "username" : "kaushikaryan",  
    "password" : "aryan@1234"  
}
---
Endpoint -> localhost:8000/api/create-group  
Payload  
{  
    "group_name" : "college-Friends",  
    "description" : "group to deal with expenses with college friends" ,  
    "members" : ["2" , "3"]  
}  
---  
Endpoint -> localhost:8000/api/expense ( GET AND POST) 
Payload ( POST )  
{  
    "group_id" : "1",  
    "expense_name" : "Movie",  
    "amount" : "600",  
    "shared_equally" : "True",  
    "split_type" : "EQUAL"   
} 
---  
Endpoint -> localhost:8000/api/settle  
Payload  
{  
    "split_id" : "1",  
    "amount" : 200  
}  



