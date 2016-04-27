def is_string(value):
    
    return isinstance(value, basestring)
    
    
def try_parse_int(value):
    
    return try_parse_int2(value, value)
    
    
def try_parse_int2(value, default):
    
    x = default
    
    try:
        x = int(value)
    except:
        pass
    
    return x
        

def get_citation_from_citation(citation):

    if citation is None or citation == '':
        return None

    return citation.translate(None, ' .').lower()


def get_citation_from_priorpub(priorpub):
    
    index = 0
    
    if is_string(priorpub) == False:
        return None
    
    strlen = len(priorpub)

    # Unhandled case
    # This is not the solution
    # Only p1 and p4 exist, how to identify p2 and p3?
    if '/' in priorpub:
        return priorpub.translate(None, '/')

    
    p1 = ''
    p2 = ''
    p3 = ''
    p4 = ''

    # P1
    # Extract numbers till char from start
    while index < strlen:

        if priorpub[index].isalpha():
            break

        p1 += priorpub[index]
        index += 1

    p1 = try_parse_int2(p1, 0)

    if p1 == 0:
        return None
    
#     print p1
    
    # P2
    # Extract ONE character
    while index < strlen:
        
        if priorpub[index].isalpha():
            p2 = priorpub[index].lower()
            break
        
        index += 1
    
    index = strlen - 1
    
    # P4
    # Extract from end
    found_num = False
    while index >= 0:
        
        if priorpub[index] == ' ':
            index -= 1
            continue
        
        if priorpub[index].isalpha():
            if found_num:
                break
        else:
            found_num = True
        
        p4 = priorpub[index] + p4
        
        index -= 1
    
    p4 = try_parse_int(p4)
    
    # P3
    found_alpha = False
    while index >= 0:
        
        if priorpub[index].isalpha():
            if found_alpha == True:
                break
            else:
                found_alpha = True
            
        if priorpub[index] == ' ':
            index -= 1
            continue
            
        
        p3 = priorpub[index] + p3
            
        index -= 1
        
    
    return str(p1) + str(p2) + str(p3) + str(p4)
