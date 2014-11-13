from interpreter.lisp_interpreter import *
import unittest 

class Test_Entire(unittest.TestCase):
	
	def test_math(self):
	 	self.assertEqual(interpret('4', Scope(library())), float(4))
		self.assertEqual(interpret('4 6', Scope(library())), float(6))
		self.assertEqual(interpret('(+ 3 2)', Scope(library())), float(5))
		self.assertEqual(interpret('(- 3 2)', Scope(library())), float(1))
		self.assertEqual(interpret('(* 3 2)', Scope(library())), float(6))
		self.assertEqual(interpret('(/ 9 2)', Scope(library())), float(4.5))
		self.assertEqual(interpret('(+ 1 1 1 1)', Scope(library())), float(4))

	def test_map(self):
		self.assertEqual(interpret('(map abs (list 1 -2 -3))', Scope(library())), [1.0, 2.0, 3.0])

	
	def test_bool(self):
		self.assertEqual(interpret('(< 10 20)', Scope(library())), True)
		self.assertEqual(interpret('(> 10 20)', Scope(library())), False)
		self.assertEqual(interpret('(= 3 2)', Scope(library())), False)
		self.assertEqual(interpret('(= 3 3)', Scope(library())), True)
		self.assertEqual(interpret('(not (< 10 (- 20 10)))', Scope(library())), True)
		self.assertEqual(interpret('(< 0 1 2 3)', Scope(library())), True)

	def test_abs(self):
		self.assertEqual(interpret('(abs -1)', Scope(library())), float(1))
		#self.assertRaises(abs_error)
	
	def test_quote(self):
		self.assertEqual(interpret('(quote hello2world)', Scope(library())), 'hello2world')
		with self.assertRaises(MyError):
			interpret('(quote 12 34)', Scope(library()))
	
	def test_list(self):
		self.assertEqual(interpret('(list 1 2 3)', Scope(library())), [1.0, 2.0, 3.0])
		self.assertEqual(interpret('(list 1 2 (list 3 4))', Scope(library())), [1.0, 2.0, [3.0, 4.0]])
		self.assertEqual(interpret('(define test (list 1 2 3)) (car test)', Scope(library())), float(1))
		self.assertEqual(interpret('(define test (list 1 2 3)) (cdr test)', Scope(library())), [2.0, 3.0])
	
	def test_def(self):
		self.assertEqual(interpret('(define (f x)(+ x 2))', Scope(library())), None)
		self.assertEqual(interpret('(define (function x y) (+ x y)) (function 4 4)', Scope(library())), float(8))
		self.assertEqual(interpret('(define (func x)(+ x 1))(func 1)', Scope(library())), float(2))
		self.assertEqual(interpret('(define x 3) (+ x 2)', Scope(library())), float(5))
		self.assertEqual(interpret('(define blah 4) blah', Scope(library())), float(4))
		self.assertEqual(interpret('(define x 3)(define x 4) x', Scope(library())), float(4))

	def test_if(self):
		self.assertEqual(interpret('(if (< 10 20) 11 12)', Scope(library())), float(11))

	def test_cond(self):
		self.assertEqual(interpret("(cond ((> 0 0) 1)(else 'bloo))", Scope(library())), "bloo")
	
	def test_lambda(self):
		self.assertEqual(interpret('((lambda (x y) (+ x y)) 5 6)', Scope(library())), float(11))
	
	def test_def_and_lambda_combination(self):
		self.assertEqual(interpret('(define add3 (lambda (x) (+ x 3))) (add3 3)', Scope(library())), float(6))

	def test_let(self):
		self.assertEqual(interpret('(let ((x 3)) x)', Scope(library())), float(3))
		self.assertEqual(interpret('(let ((x 1)(y 1)) (* x y))', Scope(library())), float(1))
		self.assertEqual(interpret('(let ((a 4) (b 3))(let ((a (* a a))(b (* b b)))(+ a b)))', Scope(library())), float(25))

	def test_set(self):
		self.assertEqual(interpret('(define x 3)(set! x 4) x', Scope(library())), float(4))

	def test_if_handles_recursion(self):
		self.assertEqual(interpret('(define (fib n) (cond ((= n 0) 0) ((= n 1) 1)'
						+ '(else (+ (fib (- n 1)) (fib (- n 2)))))) (fib 10)', Scope(library())), float(55))
		

	def test_if_handles_scheme_func(self):
		self.assertEqual(interpret('(! 3)', Scope(library())), float(6))


	def test_begin(self):
		self.assertEqual(interpret('(if (< 1 1) (+ 1 1) (begin (define x 3) x))', Scope(library())), float(3))
	