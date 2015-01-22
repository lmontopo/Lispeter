from Lisp_Interpreter.lisp_interpreter import evaluate_atom, evaluate_cons, Scope, is_number
import unittest 


class TestSmallParts(unittest.TestCase):
	
	def test_is_number(self):
		self.assertTrue(is_number(1))
		self.assertTrue(is_number(2.0))
		self.assertFalse(is_number('x'))
		self.assertFalse(is_number('+'))
	
	#Try to test the fetch and add methods of our class scope
	def test_scope_class(self):
		scope = Scope({}, None)
		inner_scope = Scope({},scope)
		scope.add_values('country','capital')
 		self.assertEqual(scope.fetch('country'), 'capital') #fetch from current scope
 		self.assertEqual(inner_scope.fetch('country'), 'capital') #fetching passed to parent

	