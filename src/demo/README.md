- valid

- example
    - scalar
        - 73: scheme_tolerance (double_min)
        - 29: balance_on (type)
    - array
        - 42: init_conc (array)
    - record
        - 4: description (ok)
        - 6: mesh (obliatory key)
    - abstract record
        - 3: TYPE (missing type, invalid type)

    - autoconvert
        - 26: output_fields (autoconvert, selection)
            - value instead of array (autoconvert)
            - validate selection DarcyMHOutput_Selection
            
        - 17: bc_type (selection)
            a) abstract record: Field:R3->Enum
            b) TYPE? not applicable
            c) default descendant: FieldConstant
            d) reducible_to_key: value
            e) value: selection DarcyFlow_BC_Type {dirichlet, neumann, robin}

- invalid