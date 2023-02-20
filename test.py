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

initial_qname = dns.name.from_text("amazon.com")
initial_query = dns.message.make_query(initial_qname, dns.rdatatype.A)
initial_response = dns.query.udp(initial_query, "199.9.14.201")

def dig_down(response,query):
    ip=""
    if response.answer:
        return response.answer

    if response.additional:
        for i in range(len(response.additional)):
            type_A= str(response.additional[i]).split()[3]
            if type_A == "A":
                ip= str(response.additional[i]).split()[4]
                break
        if ip=="":
            return "Error"
        new_response=dns.query.udp(query, ip)
        return dig_down(new_response,query)

    if response.authority:
        ip=""
        aName=str(response.authority[0]).split()[4]
        qname_a = dns.name.from_text(aName)
        query_a = dns.message.make_query(qname_a, dns.rdatatype.A)
        response_a = dns.query.udp(query_a, "199.9.14.201")
        answer=dig_down(response_a,query_a)
        ip=str(answer[0]).split()[4]
        new_resp=dns.query.udp(query, ip)
        return dig_down(new_resp,query)

    return "Error"



print("QUESTION SECTION:")
print(initial_response.question[0])
print("Answer Section:")
answer=dig_down(initial_response,initial_query)[0]
if answer == "E":
    print("ERROR")
else:
    print(answer)

while answer != "E" and str(answer).split()[3]=="CNAME":
    Cname=str(answer).split()[4]
    qname_c = dns.name.from_text(Cname)
    query_c = dns.message.make_query(qname_c, dns.rdatatype.A)
    response_c = dns.query.udp(query_c,"199.9.14.201")
    # Using Cname to dig
    answer= dig_down(response_c,query_c)[0]
    if answer == "E":
        print("ERROR")
    else:
        print(answer)

  










  





