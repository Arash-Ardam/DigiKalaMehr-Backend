

class BuildResponse:
    @classmethod
    def ForUser(self,user,totalMonths,expiration,totalPrice):
        context ={
            "id": user.id,
            "username": user.username,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "profilePhoto": f"{user.profilePhoto}",
            "phone": user.phone,
            "totalMonths": totalMonths,
            "expiration": expiration,
            "totalPrice": totalPrice
            }
        
        return context
    
