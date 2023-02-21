# Kilinc Alparslan 
# 310- Assignment 1
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import time
from datetime import datetime


# Creating mydig_output file & getting domain name from user
file1 = open("mydig_output.txt","w")
website=input("Enter Domain:")
# printing the input from user
print("INPUT:",website,file=file1)
print(" ",file=file1)
# Starting Query Time
start_time = time.time()

# Making the Initial query to the Root
initial_qname = dns.name.from_text(website)
initial_query = dns.message.make_query(initial_qname, dns.rdatatype.A)
initial_response = dns.query.udp(initial_query, "199.9.14.201")


# Our Function that will Recursively check our Response until we get an Answer 
# It will look for IP's to dig
# Algorithm follows as:  
# Check for Answer , Then check additional for IP then use this IP to ask about the query until Answer.
# If No Answer or Additional Then check Authority: Authority Algo Extracts the server name to be asked then asks it to the Root
# Inside of Authority we check if we have an Answer if not we dig_down with our authority query to get IP address then using this IP
# we ask our actual query to this IP (Not the Authoritative query) , if we have answer we return other wise we keep digging.
def dig_down(response,query,ip):
    if response.answer:
        return response.answer
    if response.additional:
        for i in range(len(response.additional)):
            type_A= str(response.additional[i]).split()[3]
            if type_A == "A":
                ip= str(response.additional[i]).split()[4]
                break
        new_response=dns.query.udp(query, ip)
        return dig_down(new_response,query,ip)

    if response.authority:
        aName=str(response.authority[0]).split()[4]
        qname_a = dns.name.from_text(aName)
        query_a = dns.message.make_query(qname_a, dns.rdatatype.A)
        response_a = dns.query.udp(query_a, "199.9.14.201")
        if response_a.answer:
            return response_a.answer
        ip_place = dig_down(response_a,query_a,"199.9.14.201")
        ip_2=str(ip_place[0]).split()[4]
        if ip == ip_2:
            return ip_place
        response_deep=dns.query.udp(query, ip_2)
        if response_deep.answer:
            return response_deep.answer
        return dig_down(response_deep,query,ip)
    return "Error"


# Printing the Question 
print("QUESTION SECTION:",file=file1)
print(initial_response.question[0],file=file1)
print("",file=file1)
print("Answer Section:",file=file1)
# Making our Initial Dig 
answer=dig_down(initial_response,initial_query,"199.9.14.201")[0]
# checking if Initial Dig Returned Error
if answer == "E":
    print("ERROR",file=file1)

# If Our Answer Returns a CNAME we need to Resolve further
while answer != "E" and str(answer).split()[3]=="CNAME":
    # Making a Query and sending it to Root
    Cname=str(answer).split()[4]
    qname_c = dns.name.from_text(Cname)
    query_c = dns.message.make_query(qname_c, dns.rdatatype.A)
    response_c = dns.query.udp(query_c,"199.9.14.201")
    # Using Cname to dig. If we get Answer that is not CNAME it will exit 
    answer= dig_down(response_c,query_c,"199.9.14.201")[0]
    # Checking for error , print then exits loop
    if answer == "E":
        print("ERROR",file=file1)


#String Manipulation to extract the LAST OUTPUT (Which is the derived answer from all the query's) from Answer in required Output Format.
answer_line =" ".join(str(answer).split()[1:])
answer_reverse= (answer_line.split())[::-1]
last_answer = answer_reverse[:4][::-1]
solution= " ".join(last_answer)

# Printing All The Data 
print(website,solution,file=file1)
print("",file=file1)
print("More Information:",file=file1)
print(answer,file=file1)
print("",file=file1)
print("Query Time:",(time.time()-start_time) ,file=file1)
print("When:",datetime.now(),file=file1)
  










  





