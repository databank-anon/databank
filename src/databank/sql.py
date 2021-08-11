from lark import Lark, Token, Tree

from .memory import Cell

with open("databank/sql.lark") as f:
    sql_lark = f.read()
    
parser = Lark(sql_lark)

def _is_token(obj, token):
    return isinstance(obj, Token) and obj.type == token

def _is_tree(obj, tree):
    return isinstance(obj, Tree) and obj.data == tree

def assert_table(s):
    if s[-1] != '_':
        raise InvalidSQLQuery("Table names cannot end in '_': '{}'.".format(s))

def resolve_table(table, query):
    if table == query.table:
        return 0
    else:
        try:
            index = [join.table for join in query.joins].index(table)
            return index + 1
        except ValueError:
            raise InvalidSQLQuery(f"Table {table} is undefined")

def table_name(idx, query):
    if idx == 0:
        return query.table
    else:
        return query.joins[idx - 1].table

class Values:

    def __init__(self, x=None, query=None, values=None):
        if x is not None:
            self.values = []
            for c in x.children:
                self.values.append(parse_expression(c, query=query))
        else:
            self.values = values

    def __str__(self):
        return "VALUES (" + ", ".join(map(str, self.values)) + ")"

    def set_params(self, params):
        for value in self.values:
            value.set_params(params)

class ResultColumns:

    def __init__(self, x=None, query=None, type_=None, columns=None):
        self.query = query
        if x is not None:
            if _is_token(x.children[0], "STAR"):
                self.type_   = "star"
                self.columns = "*"
            elif _is_token(x.children[0], "COUNTSTAR"):
                self.type_   = "countstar"
                self.columns = "COUNT(*)"
            elif _is_tree(x.children[0], "starred"):
                self.type_   = "starred"
                table = x.children[0].children[0].value
                self.columns = resolve_table(table, query)
            else:
                self.type_   = "list"
                self.columns = [parse_expression(c, query=query) for c in x.children]
        else:
            self.type_   = type_
            self.columns = columns

    def __str__(self):
        if self.type_ == "star":
            return "*"
        elif self.type_ == "countstar":
            return "COUNT(*)"
        elif self.type_ == "starred":
            return f"\"{table_name(self.columns, self.query)}\".*"
        else:
            return ", ".join(map(str, self.columns))

    def set_params(self, params):
        if self.type_ == "list":
            for column in self.columns:
                column.set_params(params)

class ColumnList:

    def __init__(self, x=None, columns=None):
        if x is not None:
            self.columns = []
            for c in x.children:
                self.columns.append(c.value)
        else:
            self.columns = columns    

    def __str__(self):
        return "(" + ", ".join(map(str, self.columns)) + ")"

    def set_params(self, params):
        pass

class Join:

    def __init__(self, x=None, query=None, type_= None, table=None, left_on=None, right_on=None):
        if x is not None:
            self.type_    = x.children[0].value
            self.table    = x.children[1].value
            self.left_on  = Col(x.children[2].children[0], query=query)
            self.right_on = Col(x.children[2].children[1], query=query)
        else:
            self.type_    = type_
            self.table    = table
            self.left_on  = left_on
            self.right_on = right_on

    def __str__(self):
        return f"{self.type_} {self.table} ON {self.left_on} = {self.right_on}"

    def set_params(self, params):
        pass

    def get_vars(self):
        return {str(self.left_on), str(self.right_on)}
        

class OrderingTerm:

    def __init__(self, x=None, query=None, key=None, order=None, nulls_order=None):
        if x is not None:
            x = x.children
            self.key = parse_expression(x[0], query=query)
            self.order = None
            self.nulls_order = None
            i = 1
            if i < len(x) and _is_token(x[i], "ORDER"):
                self.order = x[i].value
                i += 1
            if i < len(x) and _is_token(x[i], "NULLS_ORDER"):
                self.nulls_order = x[i].value
        else:
            self.key = key
            self.order = order
            self.nulls_order = nulls_order

    def __str__(self):
        q = str(self.key)
        if self.order:
            q += " " + self.order
        if self.nulls_order:
            q += " " + self.nulls_order
        return q

    def set_params(self, params):
        self.key.set_params(params)

    def get_vars(self):
        return self.key.get_vars()

class OrderBy:

    def __init__(self, x=None, terms=None, query=None):
        if x is not None:
            self.terms = []
            for c in x.children:
                self.terms.append(OrderingTerm(c, query=query))
        else:
            self.terms = terms

    def __str__(self):
        return "ORDER BY " + ", ".join(map(str, self.terms))

    def set_params(self, params):
        for term in self.terms:
            term.set_params(params)

    def get_vars(self):
        return {var for term in self.terms for var in term.get_vars()}

class Var:

    def __init__(self, x=None, name=None):
        if x is not None:
            self.name = x.children[0].value
        else:
            self.name = name

    def __str__(self):
        return self.name

    def set_params(self, params):
        pass

    def get_inputs(self):
        return {}

    def get_vars(self):
        return {self.name}

class Col:

    def __init__(self, x=None, query=None, table=None, name=None):
        self.query = query
        if x is not None:
            table = x.children[0].value
            self.name  = x.children[1].value
            if table == query.table:
                self.table = 0
            elif isinstance(query, Select):
                try:
                    index = [join.table for join in query.joins].index(x.children[0].value)
                    self.table = index + 1
                except ValueError:
                    raise InvalidSQLQuery(f"Table {table} is undefined")
            else:
                raise InvalidSQLQuery(f"Table {table} is undefined")
        else:
            self.table = table
            self.name  = name
            
    def __str__(self):
        if type(self.table) is str:
            return f"\"{self.table}\".{self.name}"
        else:
            return f"\"{table_name(self.table, self.query)}\".{self.name}"

    def set_params(self, params):
        pass

    def get_inputs(self):
        return {}

    def get_vars(self):
        return {str(self)}

class Unop:

    def __init__(self, x=None, query=None, op=None, rhs=None):
        if x is not None:
            x = x.children
            self.op = x[0].value
            self.rhs = parse_expression(x[1], query=query)
        else:
            self.op = op
            self.rhs = rhs

    def __str__(self):
        return self.op + " " + str(self.rhs)

    def set_params(self, params):
        self.rhs.set_params(params)

    def get_inputs(self):
        return self.rhs.get_inputs()

    def get_vars(self):
        return self.rhs.get_vars()

class Binop:

    def __init__(self, x=None, query=None, op=None, lhs=None, rhs=None):
        if x is not None:
            x = x.children
            self.op = x[1].value
            self.lhs = parse_expression(x[0], query=query)
            self.rhs = parse_expression(x[2], query=query)
        else:
            self.op = op
            self.lhs = lhs
            self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " " + self.op + " " + str(self.rhs)

    def set_params(self, params):
        self.lhs.set_params(params)
        self.rhs.set_params(params)

    def get_inputs(self):
        return dict(self.lhs.get_inputs(), **self.rhs.get_inputs())

    def get_vars(self):
        return self.lhs.get_vars() | self.rhs.get_vars()

class Tuple:

    def __init__(self, x=None, query=None, items=None):
        if x is not None:
            self.items = []
            for c in x.children:
                self.items.append(parse_expression(c, query=query))
        else:
            self.items = items

    def __str__(self):
        return "(" + ", ".join(map(str, self.items)) + ")"

    def set_params(self, params):
        for item in self.items:
            item.set_params(params)

    def get_inputs(self):
        d = {}
        for item in self.items:
            d = dict(d, **item.get_inputs())
        return d

    def get_vars(self):
        s = set()
        for item in self.items:
            s |= item.get_vars()
        return s
    
class NullTest:

    def __init__(self, x=None, query=None, op=None, lhs=None):
        if x is not None:
            x = x.children
            self.op = x[1].value
            self.lhs = parse_expression(x[0], query=query)
        else:
            self.op = op
            self.lhs = lhs

    def __str__(self):
        return str(self.lhs) + " " + self.op

    def set_params(self, params):
        self.lhs.set_params(params)

    def get_inputs(self):
        return self.lhs.get_inputs()

    def get_vars(self):
        return self.lhs.get_vars()

class Between:

    def __init__(self, x=None, query=None, lhs=None, mhs=None, rhs=None):
        if x is not None:
            x = x.children
            self.lhs = parse_expression(x[0], query=query)
            self.mhs = parse_expression(x[1], query=query)
            self.rhs = parse_expression(x[2], query=query)
        else:
            self.lhs = lhs
            self.mhs = rhs
            self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " BETWEEN " + str(self.mhs) + " AND " + str(self.rhs)

    def set_params(self, params):
        self.lhs.set_params(params)
        self.mhs.set_params(params)
        self.rhs.set_params(params)

    def get_inputs(self):
        return dict(dict(self.lhs.get_inputs(), **self.mhs.get_inputs()), **self.rhs.get_inputs())

    def get_vars(self):
        return self.lhs.get_vars() | self.mhs.get_vars() | self.rhs.get_vars()

class Case:

    def __init__(self, x=None, query=None, cases=None, else_=None):
        if x is not None:
            x = x.children
            self.cases = []
            self.else_ = None
            f = 0
            if _is_tree(x[-1], "else"):
                self.else_ = parse_expression(x[-1].children[0], query=query)
                f = 1
            for i in range(f-1):
                self.cases.append((parse_expression(x[i].children[0], query=query),
                                   parse_expression(x[i].children[1], query=query)))
        else:
            self.cases = cases
            self.else_ = else_

    def __str__(self):
        q = "CASE"
        for when, then in self.cases:
            q += " WHEN " + str(when) + " THEN " + str(then)
        if self.else_:
            q += " ELSE " + str(self.else_)
        return q + " END"

    def set_params(self, params):
        for when, then in self.cases:
            when.set_params(params)
            then.set_params(params)
        if self.else_ is not None:
            self.else_.set_params(params)

    def get_inputs(self):
        d = {}
        for when, then in self.cases:
            d = dict(dict(d, **when.get_inputs()), **then.get_inputs())
        if self.else_ is not None:
            d = dict(d, **self.else_.get_inputs())
        return d

    def get_vars(self):
        s = set()
        for when, then in self.cases:
            s |= when.get_vars() | then.get_vars()
        if self.else_ is not None:
            s |= s.else_.get_vars()
        return s
            
def parse_expression(x, query=None):
    x = x.children
    if _is_tree(x[0], "literal_value"):
        return Literal(x[0])
    elif _is_tree(x[0], "var"):
        return Var(x[0])
    elif _is_tree(x[0], "col"):
        return Col(x[0], query=query)
    elif _is_tree(x[0], "unop"):
        return Unop(x[0], query=query)
    elif _is_tree(x[0], "binop"):
        return Binop(x[0], query=query)
    elif _is_tree(x[0], "tuple"):
        return Tuple(x[0], query=query)
    elif _is_tree(x[0], "null_test"):
        return NullTest(x[0], query=query)
    elif _is_tree(x[0], "between"):
        return Between(x[0], query=query)
    elif _is_tree(x[0], "case"):
        return Case(x[0], query=query)

class Literal:

    def __init__(self, x=None, value=None, child=0):
        if x is not None:
            x = x.children[child]
            if x.type == "NUMERIC":
                if "." in x.value or "E" in x.value:
                    self.value = float(x.value)
                else:
                    self.value = int(x.value)
            if x.type == "NAT":
                self.value = int(x.value)
            elif x.type == "STRING":
                self.value = x.value[1:-1].replace("'", "''")
            elif x.type == "BOOLEAN":
                self.value = x.value.upper() == "TRUE"
            elif x.type == "NULL":
                self.value = None
            elif x.type == "CURRENT":
                self.value = "CURRENT", x.value
            elif x.type == "PARAM":
                self.value = "PARAM", int(x.value[1:])
        else:
            self.value = value
        self.inputs = {}

    def __str__(self):
        if type(self.value) is str:
            return "'{}'".format(self.value)
        elif type(self.value) is tuple:
            if self.value[0] == "CURRENT":
                return self.value[1]
            elif self.value[0] == "PARAM":
                return "?" + str(self.value[1])
        elif self.value is None:
            return "NULL"
        else:
            return repr(self.value)

    def set_params(self, params):
        if type(self.value) is tuple and self.value[0] == "PARAM":
            if isinstance(params, Cell):
                if self.value[1] < len(params.value):
                    value = params.value[self.value[1]].value
                    if type(value) is str:
                        value = value.replace("'", "''")
                    self.inputs = dict(params.value[self.value[1]].inputs, **params.inputs)
                    self.value  = value
            else:
                if self.value[1] < len(params):
                    value = params[self.value[1]]
                    if type(value) is str:
                        value = value.replace("'", "''")
                    self.value = value

    def get_inputs(self):
        return dict(self.inputs)

    def get_vars(self):
        return set()

class Delete:

    def __init__(self, x=None, table=None, where=None):
        if x is not None:
            x = x.children
            self.table = x[0].value
            self.where = parse_expression(x[1].children[0], query=self)
        else:
            self.table = table
            self.where = where

    def __str__(self):
        return "DELETE FROM \"" + self.table + "\" WHERE " + str(self.where)

    def set_params(self, params):
        self.where.set_params(params)

class Insert:

    def __init__(self, x=None, table=None, column_list=None):
        if x is not None:
            x = x.children
            self.table = x[0].value
            self.column_list = None
            i = 1
            if _is_tree(x[i], "column_list"):
                self.column_list = ColumnList(x[i])
                i += 1
            self.values = Values(x[i])
        else:
            self.table = table
            self.column_list = column_list
            
    def __str__(self):
        q = "INSERT INTO \"" + self.table + "\""
        if self.column_list:
            q += " " + str(self.column_list) + " "
        q += " " + str(self.values)
        return q

    def set_params(self, params):
        self.values.set_params(params)

class Select:

    def __init__(self, x=None, result_columns=None, table=None, joins=None, where=None, order_by=None, limit=None, offset=None):
        if x is not None:
            x = x.children
            self.result_columns = None
            self.table = None
            self.joins = []
            self.where = None
            self.order_by = None
            self.limit = None
            self.offset = None
            self.table = x[1].children[0].value
            i = 2
            while i < len(x) and _is_tree(x[i], "join"):
                self.joins.append(Join(table=x[i].children[1].value))
                self.joins[-1] = Join(x[i], query=self)
                i += 1
            self.result_columns = ResultColumns(x[0], query=self)
            if i < len(x) and _is_tree(x[i], "where"):
                self.where = parse_expression(x[i].children[0], query=self)
                i += 1
            if i < len(x) and _is_tree(x[i], "order_by"):
                self.order_by = OrderBy(x[i], query=self)
                i += 1
            if i < len(x) and _is_tree(x[i], "limit"):
                self.limit = Literal(x[i])
                if len(x[i].children) > 1:
                    self.offset = Literal(x[i], child=1)
        else:
            self.result_columns = result_columns
            self.table = table
            self.joins = joins or []
            self.where = where
            self.order_by = order_by
            self.limit = limit
            self.offset = offset
            
        if self.result_columns.type_ == "star" and self.joins:
            raise InvalidSQLQuery("Cannot combine * or COUNT(*) and JOIN clauses")

    def __str__(self):
        q = "SELECT " + str(self.result_columns)
        if self.table:
            q += " FROM \"" + str(self.table) + "\""
        for join in self.joins:
            q += f" {join.type_} \"{join.table}\" ON {join.left_on} = {join.right_on}"
        if self.where:
            q += " WHERE " + str(self.where)
        if self.order_by:
            q += " " + str(self.order_by)
        if self.limit:
            q += " LIMIT " + str(self.limit)
        if self.offset:
            q += " OFFSET " + str(self.offset)
        return q

    def set_params(self, params):
        self.result_columns.set_params(params)
        if self.where:
            self.where.set_params(params)
        if self.order_by:
            self.order_by.set_params(params)
        if self.limit:
            self.limit.set_params(params)
        if self.offset:
            self.offset.set_params(params)
        
class InvalidSQLQuery(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return "Invalid SQL query: " + self.message
    
def parse(query):
    try:
        parsed_query = parser.parse(query)
    except Exception as e:
        raise InvalidSQLQuery(str(e))
    head = parsed_query.children[0]
    head_cat = parsed_query.children[0].data
    if head_cat == 'select_stmt':
        return Select(head)
    elif head_cat == 'insert_stmt':
        return Insert(head)
    elif head_cat == 'delete_stmt':
        return Delete(head)
    else:
        raise InvalidSQLQuery("Query cannot be parsed as a SELECT, INSERT or DELETE statement")
