from rest_framework import serializers

from higher_edu.models import University


class UniversitySerializer(serializers.ModelSerializer):
	class Meta:
		model = University
		fields = ('name', 'description', 'short_description', 'logo')
