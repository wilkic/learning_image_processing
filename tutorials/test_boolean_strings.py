
spot = {}
spot['k'] = True
spot['e'] = False
spot['m'] = True


# Check the first one
present = True
sdt = 'k&e|m'
dt = sdt[0]
pstr = dt
present = present and spot[pstr]

# Check remaining ones if there
l = len(sdt)
if l > 1:
    detection_types = ['m','k','e']
    expr_types = ['&','|']
    
    expr = 'present=present'
    no_operator_specified = True
    for dt in sdt[1:]:
        if dt in detection_types:
            if no_operator_specified:
                expr += '&'
            else:
                no_operator_specified = True
            expr = expr + "spot['" + dt + "']"
        elif dt in expr_types:
            expr += dt
            no_operator_specified = False

        else:
            print "Unknown type: %s" % dt
            break

print "present = %r" % present
print "expr = %s" % expr
exec(expr)
print "present = %r" % present

