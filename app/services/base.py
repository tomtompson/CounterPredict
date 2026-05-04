# app/services/hltv_base.py

import logging
import random
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from fastapi import HTTPException
from lxml import etree
from requests import Response, TooManyRedirects
import requests

from app.utils.utils import trim

logger = logging.getLogger(__name__)

# ==================== HELPERS ====================

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

_SEC_CH_UA = [
    '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    '"Chromium";v="123", "Not(A:Brand";v="24", "Google Chrome";v="123"',
]

_ACCEPT_LANGUAGES = ["pt-BR,pt;q=0.9,en;q=0.8", "en-US,en;q=0.9,pt;q=0.8"]


def _get_random_headers() -> Dict[str, str]:
    """
    generate random HTTP headers to avoid fingerprinting.
    
    returns:
        dict with headers
    """
    ua = random.choice(_USER_AGENTS)
    sec_ch_ua = random.choice(_SEC_CH_UA)
    accept_lang = random.choice(_ACCEPT_LANGUAGES)
    platform = "Windows" if "Windows" in ua else "macOS"
    return {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": accept_lang,
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f'"{platform}"',
    }


# ==================== BASE CLASS ====================

@dataclass
class HLTVBase:
    """
    class for making HTTP requests to HLTV and extracting data from web pages.
    
    attributes:
        response (dict): stores the response data (results, metadata, etc.)
        use_proxy (bool): if True, proxy support can be enabled (reserved for future)
    """

    URL: str = field(init=False)
    response: dict = field(default_factory=dict, init=False)
    use_proxy: bool = field(default=False, init=False)

    # ==================== INIT METHODS ====================

    def __post_init__(self) -> None:
        """initialize the session and logging after dataclass init."""
        self._init_session()
        self._init_logging()

    def _init_session(self) -> None:
        """
        create a new HTTP session with TLS fingerprint spoofing.
        uses curl_cffi if available, otherwise falls back to cloudscraper.
        """
        try:
            from curl_cffi import requests as curl_requests
            self._session = curl_requests.Session(impersonate="chrome124")
            logger.info("using curl_cffi session with chrome 124 impersonate")
        except ImportError:
            import cloudscraper
            self._session = cloudscraper.create_scraper(
                interpreter='nodejs',
                delay=15,
                browser={"browser": "chrome", "platform": "windows", "desktop": True, "mobile": False}
            )
            logger.info("using cloudscraper fallback session")
        self._session.headers.update(_get_random_headers())

    def _init_logging(self) -> None:
        """set up a logger instance for the class."""
        self.logger = logger

    def _refresh_headers(self) -> None:
        """update session headers with a fresh random set."""
        self._session.headers.update(_get_random_headers())

    # ==================== REQUEST METHODS ====================

    def make_request(self, url: Optional[str] = None) -> Response:
        """
        perform a single HTTP GET request with fresh headers.
        
        args:
            url: target url (uses self.URL if not provided)
            
        returns:
            response object with status 2xx
            
        raises:
            HTTPException: on connection errors, redirect loops, or http errors
        """
        url = self.URL if not url else url
        self._refresh_headers()

        try:
            response = self._session.get(url, timeout=30, allow_redirects=True)
            self.logger.info(f"request to {url} - status: {response.status_code}")
            response.raise_for_status()
            return response

        except TooManyRedirects:
            raise HTTPException(status_code=404, detail=f"not found: {url}")
        except ConnectionError:
            raise HTTPException(status_code=500, detail=f"connection error: {url}")
        except requests.exceptions.HTTPError as e:
            if hasattr(e.response, 'status_code') and e.response.status_code == 403:
                raise HTTPException(status_code=403, detail=f"access forbidden: {url}")
            raise HTTPException(status_code=getattr(e.response, 'status_code', 500), detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"request error: {str(e)}")

    def request_url_bsoup(self, url: Optional[str] = None) -> BeautifulSoup:
        """
        fetch a url and parse it with beautifulsoup.
        
        args:
            url: target url (uses self.URL if not provided)
            
        returns:
            beautifulsoup object
        """
        response = self.make_request(url)
        return BeautifulSoup(response.content, "html.parser")

    def request_url_page(self, url: Optional[str] = None) -> ElementTree:
        """
        fetch a url and return an lxml elementtree for xpath queries.
        
        args:
            url: target url (uses self.URL if not provided)
            
        returns:
            lxml elementtree
        """
        bsoup = self.request_url_bsoup(url)
        return self.convert_bsoup_to_page(bsoup)

    @staticmethod
    def convert_bsoup_to_page(bsoup: BeautifulSoup) -> ElementTree:
        """
        convert beautifulsoup object to lxml elementtree.
        
        args:
            bsoup: beautifulsoup object
            
        returns:
            lxml elementtree
        """
        return etree.HTML(str(bsoup))

    # ==================== PARSING METHODS ====================

    def get_all_by_xpath(self, xpath: str, element=None) -> List[str]:
        """
        extract all text strings matching an xpath expression.
        
        args:
            xpath: xpath expression
            element: optional lxml element (uses self.page if not provided)
            
        returns:
            list of trimmed strings
        """
        try:
            target = element if element is not None else self.page
            elements = target.xpath(xpath)
            return [trim(e) for e in elements if e]
        except Exception as e:
            raise ValueError(f"xpath extraction error '{xpath}': {e}") from e

    def get_text_by_xpath(
        self,
        xpath: str,
        pos: int = 0,
        iloc: Optional[int] = None,
        iloc_from: Optional[int] = None,
        iloc_to: Optional[int] = None,
        join_str: Optional[str] = None,
        attribute: Optional[str] = None,
        element=None
    ) -> Optional[str]:
        """
        get text or attribute value from elements matching an xpath.
        
        args:
            xpath: xpath expression
            pos: position to return (default 0)
            iloc: single index to extract
            iloc_from: start index for slicing
            iloc_to: end index for slicing
            join_str: if provided, join all extracted strings with this separator
            attribute: if provided, get this attribute value instead of text
            element: optional lxml element (uses self.page if not provided)
            
        returns:
            string or None if nothing found
        """
        if not hasattr(self, "page"):
            self.page = self.request_url_page()

        base = element if element is not None else self.page
        elements = base.xpath(xpath)

        if not elements:
            return None

        def extract(e):
            if isinstance(e, etree._Element):
                if attribute:
                    return trim(e.get(attribute, ""))
                return trim(e.text) if e.text else None
            return trim(str(e)) if e else None

        extracted = [extract(e) for e in elements if extract(e)]

        if isinstance(iloc, int):
            return extracted[iloc] if iloc < len(extracted) else None
        if isinstance(iloc_from, int) and isinstance(iloc_to, int):
            extracted = extracted[iloc_from:iloc_to]
        elif isinstance(iloc_to, int):
            extracted = extracted[:iloc_to]
        elif isinstance(iloc_from, int):
            extracted = extracted[iloc_from:]

        if join_str:
            return join_str.join(extracted)
        try:
            return extracted[pos]
        except IndexError:
            return None

    def get_elements_by_xpath(self, xpath: str, element=None) -> List[etree._Element]:
        """
        return raw lxml elements matching an xpath.
        
        args:
            xpath: xpath expression
            element: optional lxml element (uses self.page if not provided)
            
        returns:
            list of lxml elements
        """
        base = element if element is not None else self.page
        try:
            return base.xpath(xpath)
        except Exception as e:
            raise ValueError(f"xpath element extraction error '{xpath}': {e}") from e

    def raise_exception_if_not_found(self, xpath: str) -> None:
        """
        raise http 404 if the xpath returns no content.
        
        args:
            xpath: xpath expression to check
        """
        if not self.get_text_by_xpath(xpath):
            raise HTTPException(status_code=404, detail=f"invalid request (url: {self.URL})")