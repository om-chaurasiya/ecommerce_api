# ecommerce_api

Authentication:
    make use of jwt token for authentication where refresh token and access 
     token will be generated for mentioned time, with the help of these 
      token 
      we can perform other authenticated operations. 

USER:
   Admin (all permission to apply crud on other profile too)
   normal user (only they can apply crud on its profile)

 CART:
     cart: one to one relation betweeen cart and user and each car has 
         unique 
           id.
     cart_item: items that get entered into cart will contain contain cartid 
                and user id, and it will have unique it too.   


   for admin : admin/
   for Register: register/
   Login       : login/
   profile view :profile/
   cart     : cart/
   add to cart : cart/add/
   remove from cart: cart/remove/<int:pk>/
   to view product : products/
   to view particular product: products/<int:pk>/
   
   
