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


qname = dns.name.from_text("amazon.com")
q = dns.message.make_query(qname, dns.rdatatype.NS)
print("The query is:")
print(q)
print("")
r = dns.query.udp(q, "8.8.8.8")
print("The response is:")
print(r)
print("")
print("The nameservers are:")
ns_rrset = r.find_rrset(r.answer, qname, dns.rdataclass.IN, dns.rdatatype.NS)
for rr in ns_rrset:
    print(rr.target)
print("")
print("")

