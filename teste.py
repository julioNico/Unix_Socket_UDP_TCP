import base64



def base64_encode(sample_string):

    sample_string_bytes = sample_string.encode("ascii")
    
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    
    print(f"Encoded string: {base64_string}")
    return base64_string


sample_string = "teste"

base64_string = base64_encode(sample_string)
print(f"Encoded string: {base64_string}")


base64_string =" R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA =="

def base64_decode(base64_string):
    base64_bytes = base64_string.encode("ascii")
    
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    
    print(f"Decoded string: {sample_string}")
    return sample_string

teste = base64_decode(sample_string)
print(teste)