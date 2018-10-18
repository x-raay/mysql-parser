# coding: utf-8

import json
import sqlparse
from sqlparse.sql import IdentifierList, Identifier,Parenthesis,Assignment,Where,Comparison
from sqlparse.tokens import Keyword
import logging

class SQLParser(object):


    @staticmethod
    def parse_sql(sql):
        tables = []
        sql_parsed = {}
        parsed = sqlparse.parse(sql)

        stmt = parsed[0]
        sql_parsed["optype"] = stmt.get_type()
        sql_parsed['table'] = stmt.get_real_name()
        for token in stmt.tokens:
            # logging.debug(stmt.token_index(token))
            # logging.debug(token.ttype)
            # logging.debug(token.value)
            if token.ttype == Keyword and token.value.upper() == "FROM":
                token_table = stmt.token_next(stmt.token_index(token),skip_ws=True, skip_cm=True)
                if token_table != None:
                    logging.debug(token_table)
                    sql_parsed['table'] = token_table[1].value
                else:
                    logging.debug("Unexpected None at %s",stmt.token_index(token)+1)
            elif token.ttype == Keyword and token.value.upper() == "INTO":
                if stmt.get_real_name()!=None:
                    token_table = stmt.token_next(stmt.token_index(token)+1,skip_ws=True, skip_cm=True)
                    if token_table != None:
                        logging.debug(token_table)
                        sql_parsed['rows'] = token_table[1].value.split(' ',1)[1].strip("()")
                    else:
                        logging.debug("Unexpected None at %s",stmt.token_index(token)+1)
                elif stmt.get_real_name()==None:
                    token_table = stmt.token_next(stmt.token_index(token)+1,skip_ws=True, skip_cm=True)
                    if token_table != None:
                        logging.debug(token_table)
                        sql_parsed['table'] = token_table[1].value
                    else:
                        logging.debug("Unexpected None at %s",stmt.token_index(token)+1)
                    token_into_cols = stmt.token_next(stmt.token_index(token)+2,skip_ws=True, skip_cm=True)
                    if token_into_cols != None:
                        # logging.debug(token_into_cols[1])
                        value_into_cols = token_into_cols[1].value
                        sql_parsed["rows"] = value_into_cols.strip("()")
                    else:
                        logging.debug("Unexpected None at %s",stmt.token_index(token)+2)
            elif token.ttype == Keyword and token.value.upper() == "VALUES":
                token_into_vals = stmt.token_next(stmt.token_index(token),skip_ws=True, skip_cm=True)
                if token_into_vals != None:
                    # logging.debug(token_into_vals[1])
                    value_into_vals = token_into_vals[1].value
                    sql_parsed["values"] = value_into_vals.strip("()")
                else:
                    logging.debug("Unexpected None at %s",stmt.token_index(token)+2)
            elif token.ttype == Keyword and token.value.upper() == "SET":
                token_set_cols = stmt.token_next(stmt.token_index(token), skip_ws=True, skip_cm=True)
                if token_set_cols != None:
                    # logging.debug(token_into_cols[1])
                    value_set_cols = token_set_cols[1].value
                    sql_parsed["rows"] = value_set_cols
                else:
                    logging.debug("Unexpected None at %s",stmt.token_index(token)+2)
                token_table = stmt.token_prev(stmt.token_index(token),skip_ws=True, skip_cm=True)
                if token_table != None:
                    logging.debug(token_table)
                    sql_parsed['table'] = token_table[1].value
                else:
                    logging.debug("Unexpected None at %s",stmt.token_index(token)+1)
            elif isinstance(token,Where):
                sql_parsed["where"] = token.value
            else:
                continue

        return sql_parsed


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logs/myapp.log',
                    filemode='w')
    sql = """INSERT INTO posts (1720,"Post 2")""";
    result = SQLParser.parse_sql(sql)
    print(json.dumps(result))
