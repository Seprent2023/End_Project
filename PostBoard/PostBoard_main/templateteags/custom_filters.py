from django import template

register = template.Library()


@register.filter()
def owner(owr):
    queryset = Posts.objects.filter(to_reg_user__reg_user=self.request.user)
    objects = Posts.objects.all()
    return queryset

