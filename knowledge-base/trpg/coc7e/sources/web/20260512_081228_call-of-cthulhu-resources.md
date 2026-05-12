---
source: https://chaosium.com/call-of-cthulhu-resources
captured_at: 2026-05-12T08:12:28.988053+00:00
namespace: trpg/coc7e
tags: [coc7e, kp, official]
---

# Web Ingestion Result

Call of Cthulhu Resources 
           
           
        
         

         
                 
        
         
         

         
            document.documentElement.className = document.documentElement.className.replace('no-js', 'js');
         
         
            window.lazySizesConfig = window.lazySizesConfig || {};
            window.lazySizesConfig.loadMode = 1;
         
          

         
         
        
          
        
          

         

 
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

fbq('set', 'autoConfig', 'false', '464830580380548');
fbq('dataProcessingOptions', []);
fbq('init', '464830580380548', {"external_id":"936ba297-5cf2-4e4a-864e-72ce3ed55fd9"});
fbq('set', 'agent', 'bigcommerce', '464830580380548');

function trackEvents() {
    var pathName = window.location.pathname;

    fbq('track', 'PageView', {}, "");

    // Search events start -- only fire if the shopper lands on the /search.php page
    if (pathName.indexOf('/search.php') === 0 && getUrlParameter('search_query')) {
        fbq('track', 'Search', {
            content_type: 'product_group',
            content_ids: [],
            search_string: getUrlParameter('search_query')
        });
    }
    // Search events end

    // Wishlist events start -- only fire if the shopper attempts to add an item to their wishlist
    if (pathName.indexOf('/wishlist.php') === 0 && getUrlParameter('added_product_id')) {
        fbq('track', 'AddToWishlist', {
            content_type: 'product_group',
            content_ids: []
        });
    }
    // Wishlist events end

    // Lead events start -- only fire if the shopper subscribes to newsletter
    if (pathName.indexOf('/subscribe.php') === 0 && getUrlParameter('result') === 'success') {
        fbq('track', 'Lead', {});
    }
    // Lead events end

    // Registration events start -- only fire if the shopper registers an account
    if (pathName.indexOf('/login.php') === 0 && getUrlParameter('action') === 'account_created') {
        fbq('track', 'CompleteRegistration', {}, "");
    }
    // Registration events end

    

    function getUrlParameter(name) {
        var cleanName = name.replace(/[\[]/, '\[').replace(/[\]]/, '\]');
        var regex = new RegExp('[\?&]' + cleanName + '=([^&#]*)');
        var results = regex.exec(window.location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }
}

if (window.addEventListener) {
    window.addEventListener("load", trackEvents, false)
}
 
   

 

 

  
 
  (function () {
    window.dataLayer = window.dataLayer || [];

    function gtag(){
        dataLayer.push(arguments);
    }

    function initGA4(event) {
         function setupGtag() {
            function configureGtag() {
                gtag('js', new Date());
                gtag('set', 'developer_id.dMjk3Nj', true);
                gtag('config', 'G-M0SR4C2Q8N');
            }

            var script = document.createElement('script');

            script.src = 'https://www.googletagmanager.com/gtag/js?id=G-M0SR4C2Q8N';
            script.async = true;
            script.onload = configureGtag;

            document.head.appendChild(script);
        }

        setupGtag();

        if (typeof subscribeOnBodlEvents === 'function') {
            subscribeOnBodlEvents('G-M0SR4C2Q8N', true);
        }

        window.removeEventListener(event.type, initGA4);
    }

    gtag('consent', 'default', {"ad_storage":"denied","ad_user_data":"denied","ad_personalization":"denied","analytics_storage":"denied","functionality_storage":"denied"})
            

    var eventName = document.readyState === 'complete' ? 'consentScriptsLoaded' : 'DOMContentLoaded';
    window.addEventListener(eventName, initGA4, false);
  })()
 

 

 

 

 

 

 
function addressSet(){
fetch('/api/storefront/checkouts/{{checkout.id}}', {credentials: 'include'})
.then(res => res.json())
.then(data => localStorage.setItem("shippingAddress2", (JSON.stringify(data.consignments[0].shippingAddress))));
}
wwPage = window.location.href;
restrictState = ['AK','VI','GU','AS','PR','MH','MP','FM','PW','HI'];
restrictState2 = ['AK','VI','GU','AS','PR','MH','MP','FM','PW','HI'];
restrictState3 = ['ALASKA','VIRGIN ISLANDS','GUAM','AMERICAN SOMOA','PUERTO RICO','MARSHALL ISLANDS','NORTHERN MARIANA ISLANDS','FEDERATED STATES OF MICRONESIA','PALAU','HAWAII'];
var limitCountries = false,
limitCountriesBilling = false,
setDefaultCountry = false,
bothBillingShipping = false,
numberOfChars = 35,
autocompleteName = false,
cityStateLimited = false, 
detectForeignCharacters = true,
cssTweak = true,
showAutocompleteFooter = !1, 
autocompleteAddressInt = !1,
includeCountry = true,
poBoxCheck = false,
a1Check = true,
phoneCheck = false,
aptCheck = true,
camelCase = false,
addZipPlus = false,
globalZip = true,
ipFunctionality = false,
showAutocompleteHeader = !1, 
geoInitialComplete = !1,
customFields = false,
strictA1 = true,
strictZip = true,
validateAddressLine2 = true,
countryWillBeSet = 'united states',
countriesShipping = 'United States|Canada|Select a country',	
countriesBilling = 'United States|Canada|Select a country',
zipDoubleCheck = false,
restrictStateEnabled = false,
phoneCheckAdded = false
postEntryCheck = false;
function loadaddrexx() {
	var _cc_url = "xxredda.s3.amazonaws.com/bcinstall/xxerdda2021.js";
	var _cc_s = document.createElement('script');
	_cc_s.type = 'text/javascript';
	_cc_s.src = (("http:" === document.location.protocol) ? "http:" : "https:") + "//" + _cc_url;
	document.getElementsByTagName("head")[0].appendChild(_cc_s);
}
if ((wwPage.indexOf("billing_address") >= 0 || wwPage.indexOf("create_account") >= 0 || wwPage.indexOf("shipping_address") >= 0 || wwPage.indexOf("checkout") >= 0) && wwPage.indexOf("confirmation") == -1 ){
if(wwPage.indexOf("create_account") >= 0){
	setTimeout(function() {
		loadaddrexx();
	}, 2000);
} else {
		loadaddrexx();
}
}
 

 


  
 window.consentManagerStoreConfig = function () { return {"storeName":"Chaosium Inc.","privacyPolicyUrl":"https:\/\/www.chaosium.com\/privacy-policy\/","writeKey":null,"improvedConsentManagerEnabled":true,"AlwaysIncludeScriptsWithConsentTag":true}; }; 
  
  
  
 
var BCData = {};
 
 !function(){var b=function(){window.__AudioEyeSiteHash = "1d941a05eab77e130da8ccfc0e320b72"; var a=document.createElement("script");a.src="https://wsmcdn.audioeye.com/aem.js";a.type="text/javascript";a.setAttribute("async","");document.getElementsByTagName("body")[0].appendChild(a)};"complete"!==document.readyState?window.addEventListener?window.addEventListener("load",b):window.attachEvent&&window.attachEvent("onload",b):b()}();  
  
 
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  
  gtag('config', 'AW-10946634859', {'allow_enhanced_conversions':true});
 
   
  

 (function() {
    function decodeBase64(base64) {
       const text = atob(base64);
       const length = text.length;
       const bytes = new Uint8Array(length);
       for (let i = 0; i  

 
(function () {
    var xmlHttp = new XMLHttpRequest();
    
    xmlHttp.open('POST', 'https://bes.gcp.data.bigcommerce.com/nobot');
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send('{"store_id":"702782","timezone_offset":"-7.0","timestamp":"2026-05-12T08:12:28.17601700Z","visit_id":"42fcabe2-fc88-42ca-8107-c5114d3c590e","channel_id":1}');
})();
 

     
     
          Sprites  

         
 
     
         Toggle menu 
     
    
     
     
         
     
         
     
         
             
                 Searc
