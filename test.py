# You will use two APIs to create a DNS request to each individual server. The first is to
# create a DNS query and the second is to send this query to the destination. Figuring out
# the right APIs is up to you, but both can be found in the library. However, as mentioned
# earlier you are not allowed to use the resolve function in the library.

# Take input domain name 
# contact root server
# contact top-level- domain
# authoritative name server

# Resolve the "A" record for the query.

# Return Errors
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query

qname = dns.name.from_text("www.cnn.com")
query = dns.message.make_query(qname, dns.rdatatype.A)
response = dns.query.udp(query, "198.41.0.4")




def dig_down(response):
    # check for answer
    if response.answer:
        return response.answer
    # dig for answer
    if response.additional:
        for i in range(len(response.additional)):
            type_A= str(response.additional[i]).split()[3]
            if type_A == "A":
                ip= str(response.additional[i]).split()[4]
                break
        new_response=dns.query.udp(query, ip)
        return dig_down(new_response)
    else:
        #have to check cName
        if response.authority:
            cName=str(response.authority[0]).split()[0]
            qName= dns.name.from_text(cName)
            que = dns.message.make_query(qName, dns.rdatatype.A)
            response = dns.query.udp(que, "198.41.0.4")
            return dig_down(response)
    return "error"


print("QUESTION SECTION:")
print(response.question[0])
print("Answer Section:")
answer=dig_down(response)[0]
print(answer)
if str(answer).split()[3]=="CNAME":
    Cname=str(answer).split()[4]
    qname = dns.name.from_text(Cname)
    query = dns.message.make_query(qname, dns.rdatatype.A)
    response = dns.query.udp(query,"198.41.0.4")
    # Using Cname to dig
    Cname_response = dig_down(response)[0]
    print(Cname_response)




  





