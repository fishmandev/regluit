from django.conf import settings
from django.conf.urls import url, include
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from regluit.core.feeds import SupporterWishlistFeed
from regluit.frontend import views 


urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"^landing/$", views.home, {'landing': True}, name="landing"),
    url(r"^next/$", views.next, name="next"),
    url(r"^supporter/(?P<supporter_username>[^/]+)/$", views.supporter, {'template_name': 'supporter.html'}, name="supporter"),
    url(r"^supporter/(?P<userlist>[^/]+)/marc/$", views.userlist_marc, name="user_marc"),
    url(r"^library/(?P<library_name>[^/]+)/$", views.library, name="library"),
    url(r"^accounts/manage/$", login_required(views.ManageAccount.as_view()), name="manage_account"),
    url(r"^search/$", views.search, name="search"),
    url(r"^privacy/$", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    url(r"^terms/$", TemplateView.as_view(template_name="terms.html"), name="terms"),
    url(r"^rightsholders/$", views.rh_tools, name="rightsholders"), 
    url(r"^rightsholders/yours/$", views.rh_tools, {'template_name': 'rh_yours.html'}, name="rh_yours"), 
    url(r"^rightsholders/campaigns/$", views.rh_tools, {'template_name': 'rh_campaigns.html'}, name="rh_campaigns"), 
    url(r"^rightsholders/works/$", views.rh_tools, {'template_name': 'rh_works.html'},name="rh_works"), 
    url(r"^rightsholders/agree/$", views.RHAgree.as_view(), name="agree"), 
    url(r"^rightsholders/programs/$", TemplateView.as_view(template_name='programs.html'), name="programs"), 
    url(r"^rightsholders/agree/submitted$", TemplateView.as_view(template_name='agreed.html'), name="agreed"), 
    url(r"^rightsholders/campaign/(?P<id>\d+)/$", views.manage_campaign, name="manage_campaign"), 
    url(r"^rightsholders/campaign/(?P<id>\d+)/results/$", views.manage_campaign, {'action': 'results'}, name="campaign_results"), 
    url(r"^rightsholders/campaign/(?P<id>\d+)/(?P<ebf>\d+)/makemobi/$", views.manage_campaign, {'action': 'makemobi'}, name="makemobi"),
    url(r"^rightsholders/campaign/(?P<id>\d+)/mademobi/$", views.manage_campaign, {'action': 'mademobi'}, name="mademobi"),
    url(r"^rightsholders/edition/(?P<work_id>\d*)/(?P<edition_id>\d*)$", views.edit_edition, {'by': 'rh'}, name="rh_edition"),
    url(r"^rightsholders/edition/(?P<edition_id>\d*)/upload/$", views.edition_uploads, name="edition_uploads"),
    url(r"^rightsholders/claim/$", login_required(views.claim), name="claim"), 
    url(r"^rightsholders/surveys/$", views.surveys, name="surveys"), 
    url(r"^rightsholders/new_survey/(?P<work_id>\d*)/?$", views.new_survey, name="new_survey"),
    url(r"^rightsholders/surveys/answers_(?P<qid>\d+)_(?P<work_id>\d*).csv$", views.export_surveys, name="survey_answers"),
    url(r"^rightsholders/surveys/summary_(?P<qid>\d+)_(?P<work_id>\d*).csv$", views.surveys_summary, name="survey_summary"),
    url(r"^rh_admin/$", views.rh_admin, name="rh_admin"),
    url(r"^rh_admin/accepted/$", views.rh_admin, {'facet': 'accepted'}, name="accepted"),
    url(r"^campaign_admin/$", views.campaign_admin, name="campaign_admin"),    
    url(r"^faq/$", views.FAQView.as_view(), {'location':'faq', 'sublocation':'all'}, name="faq"), 
    url(r"^faq/(?P<location>\w*)/$", views.FAQView.as_view(), {'sublocation':'all'}, name="faq_location"), 
    url(r"^faq/(?P<location>\w*)/(?P<sublocation>\w*)/$", views.FAQView.as_view(), name="faq_sublocation"), 
    url(r"^wishlist/$", views.wishlist, name="wishlist"),
    url(r"^msg/$", views.msg, name="msg"),
    url(r"^campaigns/(?P<facet>\w*)$", views.CampaignListView.as_view(), name='campaign_list'),
    url(r"^campaigns/(?P<facet>\w*)/marc/$", views.CampaignListView.as_view(send_marc=True), name='campaign_list_marc'),
    url(r"^lists/(?P<facet>\w*)$", views.WorkListView.as_view(),  name='work_list'),
    url(r"^lists/(?P<facet>\w*)/marc/$", views.WorkListView.as_view(send_marc=True),  name='work_list_marc'),
    url(r"^free/(?P<path>.*)/marc/$", views.FacetedView.as_view(send_marc=True),  name='faceted_list_marc'),
    url(r"^free/(?P<path>.*)/$", views.FacetedView.as_view(),  name='faceted_list'),
    url(r"^free/$", views.FacetedView.as_view(),  name='free'),
    url(r"^pid/all/(?P<pubname>\d+)$", views.ByPubView.as_view(),  name='bypubname_list'),
    url(r"^pid/(?P<facet>\w*)/(?P<pubname>\d+)$", views.ByPubView.as_view(),  name='bypubname_list'),
    url(r"^pid/(?P<facet>\w*)/(?P<pubname>\d+)/marc/$", views.ByPubView.as_view(send_marc=True),  name='bypubname_list_marc'),
    url(r"^bypub/all/(?P<pubname>.*)$", views.ByPubListView.as_view(),  name='bypub_list'),
    url(r"^bypub/(?P<facet>\w*)/(?P<pubname>.*)$", views.ByPubListView.as_view(),  name='bypub_list'),
    url(r"^unglued/(?P<facet>\w*)$", views.UngluedListView.as_view(),  name='unglued_list'),
    url(r"^unglued/(?P<facet>\w*)/marc/$", views.UngluedListView.as_view(send_marc=True),  name='unglued_list_marc'),
    url(r"^creativecommons/$", views.FacetedView.as_view(),  name='cc_list'),
    url(r"^creativecommons/(?P<path>[^\s]*)/marc/$", views.FacetedView.as_view(send_marc=True),  name='cc_list_marc'),
    url(r"^creativecommons/(?P<path>[^\s]*)$", views.FacetedView.as_view(),  name='cc_list_detail'),
    url(r"^goodreads/auth/$", views.goodreads_auth, name="goodreads_auth"),
    url(r"^goodreads/auth_cb/$", views.goodreads_cb, name="goodreads_cb"),
    url(r"^goodreads/flush/$", views.goodreads_flush_assoc, name="goodreads_flush_assoc"),
    url(r"^goodreads/load_shelf/$", views.goodreads_load_shelf, name="goodreads_load_shelf"),
    url(r"^goodreads/shelves/$", views.goodreads_calc_shelves, name="goodreads_calc_shelves"),
    url(r"^stub/", views.stub, name="stub"),
    url(r"^work/(?P<work_id>\d+)/$", views.work, name="work"),
    url(r"^work/(?P<work_id>\d+)/preview/$", views.work, {'action': 'preview'}, name="work_preview"),
    url(r"^work/(?P<work_id>\d+)/acks/$", views.work, {'action': 'acks'}, name="work_acks"),
    url(r"^work/(?P<work_id>\d+)/lockss/$", views.lockss, name="lockss"),
    url(r"^lockss/(?P<year>\d+)/$", views.lockss_manifest, name="lockss_manifest"),
    url(r"^work/(?P<work_id>\d+)/download/$", views.DownloadView.as_view(), name="download"),
    url(r"^work/(?P<work_id>\d+)/download/$", views.DownloadView.as_view(), name="thank"),
    url(r"^work/(?P<work_id>\d+)/unglued/(?P<format>\w+)/$", views.download_campaign, name="download_campaign"),
    url(r"^work/(?P<work_id>\d+)/borrow/$", views.borrow, name="borrow"),
    url(r"^work/(?P<work_id>\d+)/marc/$", views.work_marc, name="work_marc"),
    url(r"^work/(?P<work_id>\d+)/reserve/$", views.reserve, name="reserve"),
    url(r"^work/(?P<work_id>\d+)/feature/$", views.feature, name="feature"),
    url(r"^work/(?P<work_id>\d+)/kw/$", views.kw_edit, name="kw_edit"),
    url(r"^work/(?P<work_id>\d+)/merge/$", login_required(views.MergeView.as_view()), name="merge"),
    url(r"^work/(?P<work_id>\d+)/editions/$", views.work,{'action': 'editions'}, name="work_editions"),
    url(r"^work/\d+/acks/images/(?P<file_name>[\w\.]*)$", views.static_redirect_view,{'dir': 'images'}), 
    url(r"^work/(?P<work_id>\d+)/librarything/$", views.work_librarything, name="work_librarything"),
    url(r"^work/(?P<work_id>\d+)/goodreads/$", views.work_goodreads, name="work_goodreads"),
    url(r"^work/(?P<work_id>\d+)/openlibrary/$", views.work_openlibrary, name="work_openlibrary"),
    url(r"^new_edition/(?P<work_id>)(?P<edition_id>)$", views.edit_edition, name="new_edition"),
    url(r"^new_edition/(?P<work_id>\d*)/(?P<edition_id>\d*)$", views.edit_edition, name="new_edition"),
    url(r"^manage_ebooks/(?P<edition_id>\d*)$", views.manage_ebooks, name="manage_ebooks"),
    url(r"^googlebooks/(?P<googlebooks_id>.+)/$", views.googlebooks, name="googlebooks"),
    url(r"^download_ebook/(?P<ebook_id>\w+)/$", views.download_ebook, name="download_ebook"),
    url(r"^download_ebook/acq/(?P<format>\w+)/(?P<nonce>\w+)/$", views.download_acq, name="download_acq"),
    url(r"^receive_gift/(?P<nonce>\w+)/$", views.receive_gift, name="receive_gift"),
    url(r"^display_gift/(?P<gift_id>\d+)/(?P<message>newuser|existing)/$", views.display_gift, name="display_gift"),
    url(r"^gift/$", login_required(views.GiftView.as_view()), name="gift"),
    url(r"^gift/credit/(?P<token>.+)/$", login_required(views.GiftCredit.as_view()), name="gift_credit"),
    url(r"^pledge/(?P<work_id>\d+)/$", login_required(views.PledgeView.as_view(),login_url='/accounts/login/pledge/'), name="pledge"),
    url(r"^pledge/cancel/(?P<campaign_id>\d+)$", login_required(views.PledgeCancelView.as_view()), name="pledge_cancel"),
    url(r"^fund/complete/$", views.FundCompleteView.as_view(), name="pledge_complete"),
    url(r"^pledge/modified/$", login_required(views.PledgeModifiedView.as_view()), name="pledge_modified"),
    url(r"^pledge/modify/(?P<work_id>\d+)$", login_required(views.PledgeView.as_view()), name="pledge_modify"),
    url(r"^payment/donation/new$", csrf_exempt(views.NewDonationView.as_view()), name="newdonation" ),
    url(r"^payment/fund/(?P<t_id>\d+)$", views.FundView.as_view(), name="fund" ),
    url(r"^pledge/recharge/(?P<work_id>\d+)$", login_required(views.PledgeRechargeView.as_view()), name="pledge_recharge"),
    url(r"^purchase/(?P<work_id>\d+)/$", login_required(views.PurchaseView.as_view(),login_url='/accounts/login/purchase/'), name="purchase"),
    url(r"^purchase/(?P<work_id>\d+)/download/$", views.download_purchased, name="download_purchased"),
    url(r"^subjects/$", views.subjects, name="subjects"),
    url(r"^subjects/map/$", login_required(views.MapSubjectView.as_view()), name="map_subject"),
    url(r"^librarything/$", views.LibraryThingView.as_view(), name="librarything"),
    url(r"^librarything/load/$", views.librarything_load, name="librarything_load"),
    url('^404testing/$', TemplateView.as_view(template_name='404.html') ),
    url('^500testing/$', TemplateView.as_view(template_name='500.html')),
    url('^robots.txt$', TemplateView.as_view(template_name='robots.txt',content_type='text/plain')),
    url(r"^emailshare/(?P<action>\w*)/?$", views.emailshare, name="emailshare"),
    url(r"^feedback/campaign/(?P<campaign_id>\d+)/?$", views.ask_rh, name="ask_rh"),
    url(r"^feedback/$", views.feedback, name="feedback"),
    url(r"^feedback/thanks/$", TemplateView.as_view(template_name="thanks.html")),
    url(r"^about/$", TemplateView.as_view(template_name="about_main.html"),
        name="about"),
    url(r"^comments/$", views.comment, name="comment"),
    url(r"^info/(?P<template_name>[\w\.]*)$", views.InfoPageView.as_view()), 
    url(r"^info/languages/(?P<template_name>[\w\.]*)$", views.InfoLangView.as_view()), 
    url(r'^supporter/(?P<supporter>[^/]+)/feed/$', SupporterWishlistFeed()),
    url(r'^campaign_archive.js/$', views.campaign_archive_js, name="campaign_archive_js"),
    url(r"^about/(?P<facet>\w*)/$", views.about,  name="about_specific"),
    url(r"^libraries/$", TemplateView.as_view(
            template_name="libraries.html",
            get_context_data=lambda: {'site': Site.objects.get_current()}
        ),
        name="libraries"),
    url(r"^ml/status/$", views.ml_status,  name="ml_status"),
    url(r"^ml/subscribe/$", views.ml_subscribe,  name="ml_subscribe"),
    url(r"^ml/unsubscribe/$", views.ml_unsubscribe,  name="ml_unsubscribe"),
    url(r"^press/$", views.press,  name="press"),
    url(r"^press_submitterator/$", views.press_submitterator,  name="press_submitterator"),
    url(r"^accounts/edit/kindle_config/$", views.kindle_config,  name="kindle_config"),
    url(r"^accounts/edit/kindle_config/(?P<work_id>\d+)/$", views.kindle_config,  name="kindle_config_download"),
    url(r"^send_to_kindle/(?P<work_id>\d+)/(?P<javascript>\d)/$", views.send_to_kindle,  name="send_to_kindle"),
    url(r"^marc/$", TemplateView.as_view(template_name='marc.html'), name="marc"),
    url(r"^accounts/edit/marc_config/$", login_required(views.LibModeView.as_view()),  name="marc_config"),
]

if settings.DEBUG:
    urlpatterns += [
        url(r"^goodreads/$", login_required(views.GoodreadsDisplayView.as_view()), name="goodreads_display"),
        url(r"^goodreads/clear_wishlist/$", views.clear_wishlist, name="clear_wishlist"),
        url(r"^celery/clear/$", views.clear_celery_tasks, name="clear_celery_tasks"),
]