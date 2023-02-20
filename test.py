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

qname = dns.name.from_text("www.yahoo.com")
query = dns.message.make_query(qname, dns.rdatatype.A)
response = dns.query.udp(query, "199.9.14.201")

def dig_down(response,query_g):
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
        new_response=dns.query.udp(query_g, ip)
        return dig_down(new_response,query_g)

    if response.authority:
        ip=""
        aName=str(response.authority[0]).split()[4]
        qname_a = dns.name.from_text(aName)
        query_a = dns.message.make_query(qname_a, dns.rdatatype.A)
        response_a = dns.query.udp(query_a, "199.9.14.201")
        print(response_a)
        if response_a.additional:
            for i in range(len(response_a.additional)):
                type_A= str(response_a.additional[i]).split()[3]
                if type_A == "A":
                    ip= str(response_a.additional[i]).split()[4]
                    break
        if ip=="":
            return "Error"
        a_response=dns.query.udp(query_a, ip)
        return dig_down(a_response,query_g)

    return "Error"



print("QUESTION SECTION:")
print(response.question[0])
print("Answer Section:")
answer=dig_down(response,query)[0]
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

  










  





