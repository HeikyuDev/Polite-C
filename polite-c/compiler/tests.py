from django.test import TestCase


class LexerTest(TestCase):
    """Tests for the Polite-C lexer."""

    def tokenize(self, code):
        from compiler.utils.lexer import get_lexer
        lexer = get_lexer()
        lexer.input(code)
        return [(tok.type, tok.value) for tok in lexer]

    # -- Compound tokens --

    def test_hello_main_is_single_token(self):
        tokens = self.tokenize("hello main!")
        self.assertEqual(tokens, [("HELLO_MAIN", "hello main!")])

    def test_thanks_is_single_token(self):
        tokens = self.tokenize("thanks!")
        self.assertEqual(tokens, [("THANKS", "thanks!")])

    def test_please_do_this_is_single_token(self):
        tokens = self.tokenize("please do this")
        self.assertEqual(tokens, [("PLEASE_DO_THIS", "please do this")])

    def test_please_define_is_single_token(self):
        tokens = self.tokenize("please define")
        self.assertEqual(tokens, [("PLEASE_DEFINE", "please define")])

    def test_please_say_is_single_token(self):
        tokens = self.tokenize("please say")
        self.assertEqual(tokens, [("PLEASE_SAY", "please say")])

    def test_please_read_is_single_token(self):
        tokens = self.tokenize("please read")
        self.assertEqual(tokens, [("PLEASE_READ", "please read")])

    def test_if_this_happens_is_single_token(self):
        tokens = self.tokenize("if this happens")
        self.assertEqual(tokens, [("IF_HAPPENS", "if this happens")])

    def test_if_not_is_single_token(self):
        tokens = self.tokenize("if not")
        self.assertEqual(tokens, [("IF_NOT", "if not")])

    def test_please_give_back_is_single_token(self):
        tokens = self.tokenize("please give back")
        self.assertEqual(tokens, [("PLEASE_GIVE_BACK", "please give back")])

    def test_please_create_is_single_token(self):
        tokens = self.tokenize("please create")
        self.assertEqual(tokens, [("PLEASE_CREATE", "please create")])

    def test_please_ask_is_single_token(self):
        tokens = self.tokenize("please ask")
        self.assertEqual(tokens, [("PLEASE_ASK", "please ask")])

    def test_to_give_is_single_token(self):
        tokens = self.tokenize("to give")
        self.assertEqual(tokens, [("TO_GIVE", "to give")])

    # -- Reserved words --

    def test_reserved_as(self):
        tokens = self.tokenize("as")
        self.assertEqual(tokens[0], ("AS", "as"))

    def test_reserved_number(self):
        tokens = self.tokenize("number")
        self.assertEqual(tokens[0], ("TYPE_NUMBER", "number"))

    def test_reserved_floatnumber(self):
        tokens = self.tokenize("floatnumber")
        self.assertEqual(tokens[0], ("TYPE_FLOAT", "floatnumber"))

    def test_reserved_word(self):
        tokens = self.tokenize("word")
        self.assertEqual(tokens[0], ("TYPE_WORD", "word"))

    def test_reserved_class_capital(self):
        tokens = self.tokenize("Class")
        self.assertEqual(tokens[0], ("CLASS", "Class"))

    def test_reserved_class_lowercase(self):
        tokens = self.tokenize("class")
        self.assertEqual(tokens[0], ("CLASS", "class"))

    def test_reserved_finish(self):
        tokens = self.tokenize("finish")
        self.assertEqual(tokens[0], ("FINISH", "finish"))

    def test_reserved_receives(self):
        tokens = self.tokenize("receives")
        self.assertEqual(tokens[0], ("RECEIVES", "receives"))

    def test_reserved_recieves_misspelling(self):
        tokens = self.tokenize("recieves")
        self.assertEqual(tokens[0], ("RECEIVES", "recieves"))

    def test_reserved_with(self):
        tokens = self.tokenize("with")
        self.assertEqual(tokens[0], ("WITH", "with"))

    def test_reserved_to(self):
        tokens = self.tokenize("to")
        self.assertEqual(tokens[0], ("TO", "to"))

    def test_reserved_make(self):
        tokens = self.tokenize("make")
        self.assertEqual(tokens[0], ("MAKE", "make"))

    def test_reserved_equals(self):
        tokens = self.tokenize("equals")
        self.assertEqual(tokens[0], ("EQUALS", "equals"))

    def test_reserved_please_standalone(self):
        tokens = self.tokenize("please")
        self.assertEqual(tokens[0], ("PLEASE", "please"))

    def test_reserved_object(self):
        tokens = self.tokenize("object")
        self.assertEqual(tokens[0], ("OBJECT", "object"))

    # -- Literals --

    def test_number_literal(self):
        tokens = self.tokenize("42")
        self.assertEqual(tokens, [("NUMBER_LITERAL", 42)])

    def test_float_literal(self):
        tokens = self.tokenize("3.14")
        self.assertEqual(tokens, [("FLOAT_LITERAL", 3.14)])

    def test_word_literal_includes_quotes(self):
        tokens = self.tokenize('"hello"')
        self.assertEqual(tokens[0][0], "WORD_LITERAL")
        self.assertEqual(tokens[0][1], '"hello"')

    # -- Operators --

    def test_arithmetic_operators(self):
        tokens = self.tokenize("+ - * / %")
        types = [t[0] for t in tokens]
        self.assertEqual(types, ["PLUS", "MINUS", "MULT", "DIV", "MOD"])

    def test_comparison_operators(self):
        tokens = self.tokenize("== != < > <= >=")
        types = [t[0] for t in tokens]
        self.assertEqual(types, ["EQ", "NE", "LT", "GT", "LE", "GE"])

    def test_assign_vs_equality(self):
        tokens = self.tokenize("= ==")
        self.assertEqual(tokens[0][0], "ASSIGN")
        self.assertEqual(tokens[1][0], "EQ")

    def test_parentheses_and_comma(self):
        tokens = self.tokenize("( , )")
        types = [t[0] for t in tokens]
        self.assertEqual(types, ["LPAREN", "COMMA", "RPAREN"])

    # -- Comments --

    def test_comment_silently_discarded(self):
        tokens = self.tokenize('!comment: "this is ignored"')
        self.assertEqual(tokens, [])

    # -- Error handling --

    def test_invalid_character_appends_to_lexer_errors(self):
        import compiler.utils.lexer as lexer_mod
        lexer = lexer_mod.get_lexer()
        lexer.input("@")
        list(lexer)  # consume all tokens
        self.assertEqual(len(lexer_mod.lexer_errors), 1)
        self.assertIn("Mala educación léxica", lexer_mod.lexer_errors[0])
        self.assertIn("@", lexer_mod.lexer_errors[0])

    # -- Line tracking --

    def test_multiline_increments_lineno(self):
        import compiler.utils.lexer as lexer_mod
        lexer = lexer_mod.get_lexer()
        lexer.input("42\n\n99")
        tokens = list(lexer)
        self.assertEqual(tokens[0].lineno, 1)
        self.assertEqual(tokens[1].lineno, 3)

    # -- Plain identifier --

    def test_plain_identifier(self):
        tokens = self.tokenize("myVar")
        self.assertEqual(tokens, [("ID", "myVar")])


class InterpreterTest(TestCase):
    """Tests for the Polite-C interpreter."""

    def execute(self, code, inputs=None):
        from compiler.utils.interpreter import PoliteInterpreter
        interp = PoliteInterpreter()
        return interp.execute(code, inputs or {})

    def program(self, *statements):
        """Wrap statements in a minimal main block."""
        body = "\n".join(statements)
        return f"hello main! please do this\n{body}\nthanks!"

    # -- Basic output --

    def test_say_number(self):
        result = self.execute(self.program("please say 42"))
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["output"], "42")

    def test_say_string_strips_quotes(self):
        result = self.execute(self.program('please say "hello world"'))
        self.assertEqual(result["output"], "hello world")

    def test_say_addition(self):
        result = self.execute(self.program("please say 1 + 2"))
        self.assertEqual(result["output"], "3")

    def test_say_float(self):
        result = self.execute(self.program("please say 3.14"))
        self.assertEqual(result["output"], "3.14")

    # -- Variable define + assign + say --

    def test_define_number_initial_value_zero(self):
        result = self.execute(self.program(
            "please define x as number",
            "please say x",
        ))
        self.assertEqual(result["output"], "0")

    def test_define_and_assign_with_make(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 5",
            "please say x",
        ))
        self.assertEqual(result["output"], "5")

    def test_direct_assign_syntax(self):
        result = self.execute(self.program(
            "please define x as number",
            "x = 10",
            "please say x",
        ))
        self.assertEqual(result["output"], "10")

    def test_word_variable(self):
        result = self.execute(self.program(
            "please define msg as word",
            'make msg equals to "hi"',
            "please say msg",
        ))
        self.assertEqual(result["output"], "hi")

    # -- Arithmetic --

    def test_arithmetic_addition(self):
        result = self.execute(self.program("please say 10 + 3"))
        self.assertEqual(result["output"], "13")

    def test_arithmetic_subtraction(self):
        result = self.execute(self.program("please say 10 - 3"))
        self.assertEqual(result["output"], "7")

    def test_arithmetic_multiplication(self):
        result = self.execute(self.program("please say 4 * 5"))
        self.assertEqual(result["output"], "20")

    def test_arithmetic_division(self):
        result = self.execute(self.program("please say 10 / 4"))
        self.assertEqual(result["output"], "2.5")

    def test_arithmetic_modulo(self):
        result = self.execute(self.program("please say 10 % 3"))
        self.assertEqual(result["output"], "1")

    def test_division_by_zero_returns_zero(self):
        result = self.execute(self.program("please say 10 / 0"))
        self.assertEqual(result["output"], "0")

    # -- Conditionals --

    def test_if_true_branch_executes(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 5",
            "if this happens (x == 5) please do this",
            '  please say "yes"',
            "finish",
        ))
        self.assertEqual(result["output"], "yes")

    def test_if_false_else_branch_executes(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 3",
            "if this happens (x == 5) please do this",
            '  please say "yes"',
            "if not please do this",
            '  please say "no"',
            "finish",
        ))
        self.assertEqual(result["output"], "no")

    def test_if_false_no_else_produces_no_output(self):
        result = self.execute(self.program(
            "please define x as number",
            "if this happens (x == 99) please do this",
            '  please say "unreachable"',
            "finish",
        ))
        self.assertEqual(result["output"], "")

    def test_condition_not_equal(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 1",
            "if this happens (x != 0) please do this",
            '  please say "diff"',
            "finish",
        ))
        self.assertEqual(result["output"], "diff")

    def test_condition_less_than(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 3",
            "if this happens (x < 5) please do this",
            '  please say "less"',
            "finish",
        ))
        self.assertEqual(result["output"], "less")

    def test_condition_greater_than(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 10",
            "if this happens (x > 5) please do this",
            '  please say "greater"',
            "finish",
        ))
        self.assertEqual(result["output"], "greater")

    def test_condition_less_than_or_equal(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 5",
            "if this happens (x <= 5) please do this",
            '  please say "leq"',
            "finish",
        ))
        self.assertEqual(result["output"], "leq")

    def test_condition_greater_than_or_equal(self):
        result = self.execute(self.program(
            "please define x as number",
            "make x equals to 5",
            "if this happens (x >= 5) please do this",
            '  please say "geq"',
            "finish",
        ))
        self.assertEqual(result["output"], "geq")

    # -- Read / awaiting_input --

    def test_read_without_input_returns_awaiting(self):
        result = self.execute(self.program(
            "please define x as number",
            "please read x",
        ))
        self.assertEqual(result["status"], "awaiting_input")
        self.assertEqual(result["variable"], "x")

    def test_read_with_input_uses_value(self):
        result = self.execute(
            self.program(
                "please define x as number",
                "please read x",
                "please say x",
            ),
            inputs={"x": "42"},
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["output"], "42")

    # -- Multi-statement output --

    def test_two_say_statements_joined_by_newline(self):
        result = self.execute(self.program(
            "please say 1",
            "please say 2",
        ))
        self.assertEqual(result["output"], "1\n2")

    # -- Classes and objects --

    def test_class_method_returns_value(self):
        code = (
            "Class Adder please do this\n"
            "  please define result as number\n"
            "  add receives(a as number, b as number)"
            " to give number please do this\n"
            "    make result equals to a + b\n"
            "    please give back result\n"
            "  finish\n"
            "finish\n"
            "hello main! please do this\n"
            "  please define calc as Adder\n"
            "  please create object calc\n"
            "  please say please ask calc to add with (3, 4)\n"
            "thanks!"
        )
        result = self.execute(code)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["output"], "7")

    # -- Error handling --

    def test_syntax_error_missing_thanks(self):
        code = "hello main! please do this\nplease say 42"
        result = self.execute(code)
        self.assertEqual(result["status"], "completed")
        self.assertIn("Error", result["output"])

    def test_invalid_character_reports_lexer_error(self):
        code = "hello main! please do this please say 42 @ thanks!"
        result = self.execute(code)
        self.assertEqual(result["status"], "completed")
        self.assertIn("Mala educación léxica", result["output"])
