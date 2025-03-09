from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem, Shipping

class CartTestCase(TestCase):
    def setUp(self):
  
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(
            name='Test Product',
            price=50.00,
            description='Test Description',
            picture='products/test.jpg',
            stock=10
        )

    def test_add_to_cart(self):

        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('add_product', args=[self.product.id]))
        
        self.assertEqual(response.status_code, 302)


        cart = Cart.objects.get(user=self.user)
        self.assertTrue(CartItem.objects.filter(cart=cart, product=self.product).exists())

    def test_update_quantity(self):
        self.client.login(username='testuser', password='password123')
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

 
        response = self.client.post(reverse('update_quantity', args=[self.product.id]), {'action': 'increase'})
        self.assertEqual(response.status_code, 302)
        

        item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(item.quantity, 2)

        response = self.client.post(reverse('update_quantity', args=[self.product.id]), {'action': 'decrease'})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)

    def test_delete_product(self):
        self.client.login(username='testuser', password='password123')
        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)


        self.assertFalse(CartItem.objects.filter(cart=cart, product=self.product).exists())

    def test_checkout(self):
        self.client.login(username='testuser', password='password123')
        

        cart, _ = Cart.objects.get_or_create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)


        shipping = Shipping.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            address='123 Test Street',
            phone='1234567890'
        )


        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'address': '123 Test Street',
            'phone': '1234567890'
        })

        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Order.objects.filter(user=self.user).exists())


        order = Order.objects.get(user=self.user)
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order.orderitem_set.first().quantity, 2)

    def test_order_history(self):
        self.client.login(username='testuser', password='password123')
        

        shipping = Shipping.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            address='123 Test Street',
            phone='1234567890'
        )
        
        order = Order.objects.create(user=self.user, shipping=shipping)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)

    
        response = self.client.get(reverse('order_history'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order #')
        self.assertContains(response, self.product.name)
