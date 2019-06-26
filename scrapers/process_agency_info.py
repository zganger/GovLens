import requests, os, json
from scrape_social_info import ScrapeSocialInfo
# from lighthouse import get_lighthouse_results
from agency_dataaccessor import AgencyDataAccessor


class ProcessAgencyInfo:

    def __init__(self, agency):
        self.agency_firms = []
        self.agency = agency
        self.website = agency['website']
        self.buckets = ["security_and_privacy","outreach_and_communication","website_accessibility"]

    def process_agency_info(self):
        try:
            agency_url = self.agency.get('website',None)
            if agency_url is None or agency_url == '':
                print(f"Website url is not available for {self.agency['id']}, name: {self.agency['name']}")
                return
            print(f"Scraping the website {agency_url}")
            page = requests.get(agency_url, timeout=30)
            scrape_social_info = ScrapeSocialInfo(page, self.website)
            social_media_info, contact_info = scrape_social_info.scrape_info()
            profile_info = {}
            for bucket in self.buckets:
                if bucket == "security_and_privacy":
                    profile_info[bucket] = self.get_security_privacy_info(self.website)
                elif bucket == "outreach_and_communication":
                    profile_info[bucket] = self.get_outreach_communication_info(social_media_info, contact_info)
                elif bucket == "website_accessibility":
                    # profile_info[bucket] = self.get_website_accessibility_info(self.website)
                    profile_info[bucket] = {}

            agency_details = {
                "id": self.agency['id'],
                "name": self.agency['name'],
                "Website": self.website,
                "profile": profile_info
                }
            
            data_accessor = AgencyDataAccessor(None, self.agency)
            data_accessor.update_scrape_info(agency_details)
            return agency_details
        except Exception as ex:
            print(f"An error occurred while processing the agency information: {str(ex)}")
    

    
    def get_security_privacy_info(self, url):
        return {
            "https": self.get_http_acess(url),
            "privacy_policies": self.get_random_value("comprehensive")
        }

    def get_website_accessibility_info(self,url):
        return {
            "mobile_friendly": self.get_random_value("test"),
            "page_speed": self.get_random_value("page_speed"),
            "performance": self.get_site_performance(url),
            "multi_lingual": self.get_random_value("multi_lingual")
        }
    
    def get_outreach_communication_info(self, social_media_info, contact_info):
        agency_info = {
            "social_media_access": self.get_socialmedia_access(social_media_info),
            "contact_access": self.get_contact_access(contact_info)
        }
        return agency_info

    def get_contact_access(self, contact_info):
        is_contact_info_available = False
        if contact_info and contact_info["phone_number"] or contact_info["email"] or contact_info["address"]:
            is_contact_info_available = True
        else:
            is_contact_info_available = False
        return self.get_criteria_object(contact_info, is_contact_info_available)
    
    def get_socialmedia_access(self, social_media_info):
        is_criteria_met = True if social_media_info and len(social_media_info) > 0 else False
        return self.get_criteria_object(social_media_info, is_criteria_met)
    
    def get_http_acess(self, url):
        return self.get_criteria_object(None, "https" in url)

    def get_random_value(self, url):
        return self.get_criteria_object(None, True)

    def get_site_performance(self, url):
        print("hello world")
        # response = get_lighthouse_results(url,'performance')
        # score = response['lighthouseResult']['categories']['performance']['score']
        # is_criteria_met = True if score >= 80 else False
        # return self.get_criteria_object(score, is_criteria_met)

    def get_criteria_object(self, criteria, is_met):
        return {
             "met_criteria" : is_met,
             "info": criteria
         }


# agency_info = ProcessAgencyInfo()
# agency_info.process_agency_info()
