from api.models import Partner

def get_all_partners():
	return Partner.objects.all()
