


from rest_framework import serializers

from .models import Profile, Skills, User



class UserSerializers(serializers.Serializer):
    class Meta:
        model = User
        fields = ['url','id','username','email']
        

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Skills
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillsSerializer(many =True,read_only=True)
    class Meta:
        model =Profile
        fields = '__all__'
        
        

        
        
class SignUpSerializer(serializers.Serializer):
    username =  serializers.CharField(max_length =150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only =True)
    
    
    def create(self,validated_data):
        
        user = User(
            username =validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model=User
        fields = ['username','email','password']
        
    
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        
        email = data.get('email') 
        password = data.get('password') 
        
        
        if email and password :
            
            user = User.objects.get(email=email)
            
            if not user:
                raise serializers.ValidationError("data is not True ")
        else:
            raise serializers.ValidationError("email and password are requiered")
        
        data['user'] =user
        return data
    
    
    