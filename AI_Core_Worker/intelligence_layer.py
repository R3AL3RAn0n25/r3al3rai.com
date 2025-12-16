"""
R3ÆLƎR AI: Intelligence Layer
Wraps Storage Facility with advanced AI capabilities WITHOUT modifying the database
"""

import requests
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import hashlib
from collections import defaultdict
import re

logger = logging.getLogger(__name__)

# ========== CIRCUIT BREAKER ==========
class CircuitBreaker:
    """Prevents cascading failures when external services fail"""
    
    def __init__(self, fail_max=5, reset_timeout=60):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_count = 0
        self.last_fail_time = None
        self.state = 'closed'  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        # Check if circuit should reset
        if self.state == 'open':
            if time.time() - self.last_fail_time >= self.reset_timeout:
                self.state = 'half_open'
                logger.info("Circuit breaker entering half-open state")
            else:
                raise CircuitBreakerError("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset if was in half_open
            if self.state == 'half_open':
                self.state = 'closed'
                self.fail_count = 0
                logger.info("Circuit breaker closed after successful call")
            
            return result
            
        except Exception as e:
            self.fail_count += 1
            self.last_fail_time = time.time()
            
            if self.fail_count >= self.fail_max:
                self.state = 'open'
                logger.error(f"Circuit breaker opened after {self.fail_count} failures")
            
            raise e

class CircuitBreakerError(Exception):
    pass


# ========== INTENT CLASSIFIER ==========
class IntentClassifier:
    """Classify user intent to route queries to appropriate handlers"""
    
    def __init__(self):
        self.intent_patterns = {
            'crypto_price': [
                r'\b(price|cost|value)\b.*\b(bitcoin|btc|ethereum|eth|crypto)\b',
                r'\b(bitcoin|btc|ethereum|eth)\b.*\b(price|cost|worth)\b',
                r'how much.*\b(bitcoin|crypto)\b'
            ],
            'security_vulnerability': [
                r'\b(cve|vulnerability|exploit|breach|hack)\b',
                r'\b(security|exploit|vulnerability)\b.*\b(recent|latest|new)\b',
                r'\b(patch|fix)\b.*\b(vulnerability|security)\b'
            ],
            'code_generation': [
                r'\b(write|create|generate)\b.*\b(code|function|script|program)\b',
                r'\b(how to code|programming|script)\b',
                r'\b(python|javascript|bash)\b.*\b(example|code)\b'
            ],
            'tool_recommendation': [
                r'\b(best tool|suggest tool|tool for|which tool)\b',
                r'\b(how to|tutorial)\b.*\b(tool|software|program)\b',
                r'\b(recommend|suggestion)\b.*\b(tool|software)\b'
            ],
            'comparison': [
                r'\b(vs|versus|compare|difference between)\b',
                r'\b(better|best)\b.*\b(or|vs)\b',
                r'\bwhich is (better|best|faster)\b'
            ],
            'news_trends': [
                r'\b(latest|recent|new|trending)\b.*\b(news|trend|update)\b',
                r'\bwhat.*happening\b',
                r'\b(current|today).*\b(news|events)\b'
            ],
            'knowledge_search': [
                r'\b(what is|explain|tell me about|define)\b',
                r'\b(how does|how do)\b',
                r'\b(why|when|where|who)\b'
            ],
            'code_repository': [
                r'\b(github|repository|repo|code)\b.*\b(search|find|look)\b',
                r'\b(best|popular|trending)\b.*\b(repo|repository|github)\b',
                r'\b(github|git)\b.*\b(project|code)\b'
            ],
            'programming_qa': [
                r'\b(stack overflow|stackoverflow|programming)\b.*\b(question|answer|help)\b',
                r'\b(how to|error|problem)\b.*\b(code|programming|script)\b',
                r'\b(debug|fix|solution)\b.*\b(code|programming)\b'
            ],
            'cybersecurity_tactics': [
                r'\b(mitre|att&ck|attack)\b.*\b(technique|tactic|framework)\b',
                r'\b(cyber|security)\b.*\b(tactic|technique|adversary)\b',
                r'\b(attack|threat)\b.*\b(pattern|method|technique)\b'
            ],
            'financial_filings': [
                r'\b(sec|edgar|filing|10-k|10-q)\b',
                r'\b(company|corporate)\b.*\b(filing|report|financial)\b',
                r'\b(stock|security)\b.*\b(filing|report)\b'
            ],
            'stock_market_data': [
                r'\b(stock|market|trading|finance)\b.*\b(data|price|chart)\b',
                r'\b(technical|indicator|analysis)\b.*\b(stock|market)\b',
                r'\b(alpha vantage|stock)\b.*\b(api|data)\b'
            ]
        }
    
    def classify(self, query: str) -> str:
        """Classify query intent"""
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        return 'knowledge_search'  # Default


# ========== EXTERNAL DATA SOURCES ==========
class ExternalDataAggregator:
    """Fetch live data from external APIs without touching Storage Facility"""
    
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 300  # 5 minutes
        self.circuit_breakers = {}
    
    def get_breaker(self, source_name):
        """Get or create circuit breaker for source"""
        if source_name not in self.circuit_breakers:
            self.circuit_breakers[source_name] = CircuitBreaker(fail_max=3, reset_timeout=60)
        return self.circuit_breakers[source_name]
    
    def fetch_crypto_price(self, symbol='bitcoin'):
        """Fetch live crypto price from CoinGecko (free, no API key)"""
        cache_key = f'crypto_{symbol}'
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        breaker = self.get_breaker('coingecko')
        
        try:
            def fetch():
                url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true'
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            # Cache result
            self.cache[cache_key] = (data, time.time())
            
            return {
                'source': 'CoinGecko',
                'symbol': symbol,
                'price_usd': data.get(symbol, {}).get('usd', 'N/A'),
                'change_24h': data.get(symbol, {}).get('usd_24h_change', 'N/A'),
                'timestamp': datetime.now().isoformat()
            }
            
        except CircuitBreakerError:
            logger.warning(f"CoinGecko circuit breaker open")
            return {'error': 'Service temporarily unavailable (circuit breaker open)'}
        except Exception as e:
            logger.error(f"Failed to fetch crypto price: {e}")
            return {'error': str(e)}
    
    def fetch_cve_data(self, search_term='recent'):
        """Fetch recent CVEs from NIST NVD (free, public API)"""
        cache_key = f'cve_{search_term}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 3600:  # 1 hour cache for CVEs
                return cached_data
        
        breaker = self.get_breaker('nvd')
        
        try:
            def fetch():
                # NVD API v2 (free, no key for basic queries)
                url = 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5'
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            vulnerabilities = data.get('vulnerabilities', [])
            
            result = {
                'source': 'NIST NVD',
                'count': len(vulnerabilities),
                'recent_cves': [
                    {
                        'id': vuln['cve']['id'],
                        'description': vuln['cve']['descriptions'][0]['value'][:200] + '...',
                        'severity': vuln['cve'].get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseSeverity', 'N/A')
                    }
                    for vuln in vulnerabilities[:5]
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("NVD circuit breaker open")
            return {'error': 'CVE service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Failed to fetch CVE data: {e}")
            return {'error': str(e)}
    
    def fetch_wikipedia_summary(self, topic):
        """Fetch Wikipedia summary"""
        cache_key = f'wiki_{topic}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 86400:  # 24 hour cache
                return cached_data
        
        breaker = self.get_breaker('wikipedia')
        
        try:
            def fetch():
                url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{topic}'
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            result = {
                'source': 'Wikipedia',
                'title': data.get('title', topic),
                'summary': data.get('extract', 'No summary available'),
                'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'timestamp': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("Wikipedia circuit breaker open")
            return None
        except Exception as e:
            logger.error(f"Failed to fetch Wikipedia data: {e}")
            return None
    
    def fetch_github_repos(self, query, sort='stars', order='desc'):
        """Fetch GitHub repositories based on search query"""
        cache_key = f'github_{query}_{sort}_{order}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 1800:  # 30 min cache
                return cached_data
        
        breaker = self.get_breaker('github')
        
        try:
            def fetch():
                url = f'https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page=5'
                headers = {'Accept': 'application/vnd.github.v3+json'}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            repos = data.get('items', [])[:5]
            result = {
                'source': 'GitHub',
                'query': query,
                'total_count': data.get('total_count', 0),
                'repositories': [
                    {
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'description': repo['description'] or 'No description',
                        'stars': repo['stargazers_count'],
                        'language': repo['language'],
                        'url': repo['html_url'],
                        'updated_at': repo['updated_at']
                    }
                    for repo in repos
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("GitHub circuit breaker open")
            return {'error': 'GitHub service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Failed to fetch GitHub data: {e}")
            return {'error': str(e)}
    
    def fetch_stack_overflow(self, query, sort='relevance', order='desc'):
        """Fetch Stack Overflow questions and answers"""
        cache_key = f'stackoverflow_{query}_{sort}_{order}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 3600:  # 1 hour cache
                return cached_data
        
        breaker = self.get_breaker('stackoverflow')
        
        try:
            def fetch():
                url = f'https://api.stackexchange.com/2.3/search?order={order}&sort={sort}&intitle={query}&site=stackoverflow&pagesize=5'
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            questions = data.get('items', [])[:5]
            result = {
                'source': 'Stack Overflow',
                'query': query,
                'total_questions': len(questions),
                'questions': [
                    {
                        'title': q['title'],
                        'link': q['link'],
                        'score': q['score'],
                        'answer_count': q['answer_count'],
                        'tags': q['tags'][:3],  # Top 3 tags
                        'creation_date': datetime.fromtimestamp(q['creation_date']).isoformat()
                    }
                    for q in questions
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("Stack Overflow circuit breaker open")
            return {'error': 'Stack Overflow service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Failed to fetch Stack Overflow data: {e}")
            return {'error': str(e)}
    
    def fetch_mitre_attack(self, technique_id=None):
        """Fetch MITRE ATT&CK framework data"""
        cache_key = f'mitre_{technique_id or "overview"}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 86400:  # 24 hour cache
                return cached_data
        
        breaker = self.get_breaker('mitre')
        
        try:
            def fetch():
                if technique_id:
                    url = f'https://attack.mitre.org/api/techniques/{technique_id}'
                else:
                    url = 'https://attack.mitre.org/api/techniques?limit=5'
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            if technique_id:
                result = {
                    'source': 'MITRE ATT&CK',
                    'technique_id': data.get('technique_id'),
                    'name': data.get('name'),
                    'description': data.get('description', 'No description'),
                    'tactics': [t['name'] for t in data.get('tactics', [])],
                    'platforms': data.get('platforms', []),
                    'url': f"https://attack.mitre.org/techniques/{technique_id}",
                    'timestamp': datetime.now().isoformat()
                }
            else:
                techniques = data.get('techniques', [])[:5]
                result = {
                    'source': 'MITRE ATT&CK',
                    'total_techniques': len(techniques),
                    'recent_techniques': [
                        {
                            'id': t['technique_id'],
                            'name': t['name'],
                            'description': t['description'][:200] + '...' if len(t['description']) > 200 else t['description'],
                            'tactics': [tac['name'] for tac in t.get('tactics', [])]
                        }
                        for t in techniques
                    ],
                    'timestamp': datetime.now().isoformat()
                }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("MITRE ATT&CK circuit breaker open")
            return {'error': 'MITRE ATT&CK service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Failed to fetch MITRE ATT&CK data: {e}")
            return {'error': str(e)}
    
    def fetch_sec_filings(self, company_symbol=None, filing_type='10-K'):
        """Fetch SEC EDGAR filings"""
        cache_key = f'sec_{company_symbol or "recent"}_{filing_type}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 3600:  # 1 hour cache
                return cached_data
        
        breaker = self.get_breaker('sec')
        
        try:
            def fetch():
                if company_symbol:
                    # Search for specific company
                    url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={company_symbol}&type={filing_type}&dateb=&owner=exclude&count=5'
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    # Note: This returns HTML, would need parsing for full implementation
                    return {'html_response': response.text[:1000]}
                else:
                    # Recent filings
                    url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type={filing_type}&company=&dateb=&owner=include&accno=&state=&country=&SIC=&mycompany=&FilingDate=&filenum=&RSS=1'
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    return {'html_response': response.text[:1000]}
            
            data = breaker.call(fetch)
            
            result = {
                'source': 'SEC EDGAR',
                'company': company_symbol,
                'filing_type': filing_type,
                'note': 'HTML response parsing needed for full implementation',
                'sample_data': data.get('html_response', ''),
                'url': f'https://www.sec.gov/edgar/searchedgar/companysearch.html',
                'timestamp': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("SEC EDGAR circuit breaker open")
            return {'error': 'SEC EDGAR service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Failed to fetch SEC EDGAR data: {e}")
            return {'error': str(e)}
    
    def fetch_alpha_vantage(self, symbol='IBM', function='TIME_SERIES_DAILY'):
        """Fetch Alpha Vantage stock data (requires API key)"""
        # Note: This would require an API key for full functionality
        cache_key = f'alphavantage_{symbol}_{function}'
        
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < 300:  # 5 min cache
                return cached_data
        
        breaker = self.get_breaker('alphavantage')
        
        try:
            def fetch():
                # Demo API key - replace with real key for production
                api_key = 'demo'  # Replace with actual API key
                url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            
            data = breaker.call(fetch)
            
            if 'Error Message' in data:
                return {'error': 'Alpha Vantage API key required for full functionality'}
            
            result = {
                'source': 'Alpha Vantage',
                'symbol': symbol,
                'function': function,
                'data': data,
                'note': 'API key required for production use',
                'timestamp': datetime.now().isoformat()
            }
            
            self.cache[cache_key] = (result, time.time())
            return result
            
        except CircuitBreakerError:
            logger.warning("Alpha Vantage circuit breaker open")
            return {'error': 'Alpha Vantage service temporarily unavailable'}
        except Exception as e:
            logger.error(f"Failed to fetch Alpha Vantage data: {e}")
            return {'error': str(e)}
    
    def aggregate_data(self, query: str) -> List[Dict[str, Any]]:
        """Aggregate external data based on query content"""
        query_lower = query.lower()
        results = []
        
        # Crypto-related queries
        if any(word in query_lower for word in ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'price', 'market']):
            crypto_data = self.fetch_crypto_price('bitcoin')
            if crypto_data and 'error' not in crypto_data:
                results.append(crypto_data)
        
        # Security/Cybersecurity queries
        if any(word in query_lower for word in ['cve', 'vulnerability', 'exploit', 'security', 'hack']):
            cve_data = self.fetch_cve_data()
            if cve_data and 'error' not in cve_data:
                results.append(cve_data)
        
        # Programming/Development queries
        if any(word in query_lower for word in ['github', 'repository', 'repo', 'code']):
            github_data = self.fetch_github_repos(query.split()[-1] if len(query.split()) > 1 else 'python')
            if github_data and 'error' not in github_data:
                results.append(github_data)
        
        # Programming Q&A queries
        if any(word in query_lower for word in ['how to', 'error', 'problem', 'debug', 'fix']):
            stack_data = self.fetch_stack_overflow(query)
            if stack_data and 'error' not in stack_data:
                results.append(stack_data)
        
        # Cybersecurity tactics
        if any(word in query_lower for word in ['mitre', 'att&ck', 'technique', 'tactic']):
            mitre_data = self.fetch_mitre_attack()
            if mitre_data and 'error' not in mitre_data:
                results.append(mitre_data)
        
        return results


# ========== HYBRID SEARCH ENGINE ==========
class HybridSearchEngine:
    """Combines Storage Facility (static knowledge) with live external data"""
    
    def __init__(self, storage_facility_url='http://localhost:5003'):
        self.storage_url = storage_facility_url
        self.intent_classifier = IntentClassifier()
        self.external_data = ExternalDataAggregator()
        self.storage_breaker = CircuitBreaker(fail_max=10, reset_timeout=30)
    
    def search(self, query: str, user_id: Optional[str] = None, max_results: int = 5) -> Dict[str, Any]:
        """
        Hybrid search: Storage Facility (30,657 entries) + Live External Data
        Does NOT modify the database - only reads and augments
        """
        start_time = time.time()
        
        # 1. Classify intent
        intent = self.intent_classifier.classify(query)
        logger.info(f"Classified query '{query}' as intent: {intent}")
        
        # 2. Search Storage Facility (your existing 30,657 entries)
        storage_results = self._search_storage_facility(query, max_results * 2)
        
        # 3. Fetch external data based on intent (WITHOUT modifying database)
        external_results = self._fetch_external_data(query, intent)
        
        # 4. Merge results
        merged_results = self._merge_results(
            storage_results,
            external_results,
            intent
        )
        
        # 5. Rank and return top results
        final_results = merged_results[:max_results]
        
        response_time = (time.time() - start_time) * 1000
        
        return {
            'success': True,
            'query': query,
            'intent': intent,
            'storage_results_count': len(storage_results),
            'external_data_included': len(external_results) > 0,
            'results': final_results,
            'response_time_ms': round(response_time, 2),
            'sources': {
                'storage_facility': True,
                'external_apis': list(external_results.keys()) if external_results else []
            }
        }
    
    def _search_storage_facility(self, query: str, limit: int) -> List[Dict]:
        """Query existing Storage Facility - NO MODIFICATIONS"""
        try:
            def fetch():
                response = requests.post(
                    f'{self.storage_url}/api/facility/search',
                    json={'query': query, 'limit_per_unit': limit},
                    timeout=5
                )
                response.raise_for_status()
                return response.json()
            
            data = self.storage_breaker.call(fetch)
            return data.get('results', [])
            
        except CircuitBreakerError:
            logger.error("Storage Facility circuit breaker open")
            return []
        except Exception as e:
            logger.error(f"Storage Facility error: {e}")
            return []
    
    def _fetch_external_data(self, query: str, intent: str) -> Dict[str, Any]:
        """Fetch live external data based on intent"""
        external_data = {}
        
        if intent == 'crypto_price':
            # Extract crypto symbol
            symbols = ['bitcoin', 'ethereum', 'btc', 'eth']
            for symbol in symbols:
                if symbol in query.lower():
                    crypto_data = self.external_data.fetch_crypto_price(symbol)
                    if crypto_data and 'error' not in crypto_data:
                        external_data['crypto'] = crypto_data
                    break
        
        elif intent == 'security_vulnerability':
            cve_data = self.external_data.fetch_cve_data()
            if cve_data and 'error' not in cve_data:
                external_data['cve'] = cve_data
        
        elif intent in ['knowledge_search', 'news_trends']:
            # Extract main topic
            topic = self._extract_topic(query)
            if topic:
                wiki_data = self.external_data.fetch_wikipedia_summary(topic)
                if wiki_data:
                    external_data['wikipedia'] = wiki_data
        
        elif intent == 'code_repository':
            # Extract search terms for GitHub
            search_terms = self._extract_code_terms(query)
            if search_terms:
                github_data = self.external_data.fetch_github_repos(search_terms)
                if github_data and 'error' not in github_data:
                    external_data['github'] = github_data
        
        elif intent == 'programming_qa':
            # Extract programming question terms
            qa_terms = self._extract_qa_terms(query)
            if qa_terms:
                so_data = self.external_data.fetch_stack_overflow(qa_terms)
                if so_data and 'error' not in so_data:
                    external_data['stackoverflow'] = so_data
        
        elif intent == 'cybersecurity_tactics':
            # Check if specific technique ID mentioned
            technique_id = self._extract_technique_id(query)
            mitre_data = self.external_data.fetch_mitre_attack(technique_id)
            if mitre_data and 'error' not in mitre_data:
                external_data['mitre'] = mitre_data
        
        elif intent == 'financial_filings':
            # Extract company symbol or filing type
            company_symbol = self._extract_company_symbol(query)
            sec_data = self.external_data.fetch_sec_filings(company_symbol)
            if sec_data and 'error' not in sec_data:
                external_data['sec'] = sec_data
        
        elif intent == 'stock_market_data':
            # Extract stock symbol
            stock_symbol = self._extract_stock_symbol(query)
            if stock_symbol:
                av_data = self.external_data.fetch_alpha_vantage(stock_symbol)
                if av_data and 'error' not in av_data:
                    external_data['alphavantage'] = av_data
        
        return external_data
    
    def _extract_topic(self, query: str) -> Optional[str]:
        """Extract main topic from query"""
        # Remove common question words
        words = query.lower().split()
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'why', 'when', 'where', 'who', 'tell', 'me', 'about'}
        
        topic_words = [w for w in words if w not in stop_words and len(w) > 3]
        
        if topic_words:
            return topic_words[0]  # Return first significant word
        
        return None
    
    def _extract_code_terms(self, query: str) -> Optional[str]:
        """Extract code-related search terms for GitHub"""
        # Look for programming languages, frameworks, or general terms
        code_keywords = ['python', 'javascript', 'java', 'c++', 'react', 'django', 'flask', 'machine learning', 'ai', 'web', 'mobile']
        query_lower = query.lower()
        
        for keyword in code_keywords:
            if keyword in query_lower:
                return keyword
        
        # Return first word after common prefixes
        words = query_lower.split()
        for i, word in enumerate(words):
            if word in ['find', 'search', 'github', 'repo', 'code']:
                if i + 1 < len(words):
                    return words[i + 1]
        
        return 'python'  # Default fallback
    
    def _extract_qa_terms(self, query: str) -> Optional[str]:
        """Extract programming question terms for Stack Overflow"""
        # Remove question words and extract key technical terms
        words = query.lower().split()
        stop_words = {'how', 'to', 'do', 'i', 'fix', 'error', 'problem', 'in', 'with', 'using', 'what', 'is', 'the'}
        
        tech_terms = [w for w in words if w not in stop_words and len(w) > 2]
        
        if tech_terms:
            return ' '.join(tech_terms[:3])  # First 3 technical terms
        
        return None
    
    def _extract_technique_id(self, query: str) -> Optional[str]:
        """Extract MITRE ATT&CK technique ID if mentioned"""
        # Look for patterns like T1059, T1059.001, etc.
        import re
        pattern = r'\bT\d{4}(\.\d{3})?\b'
        match = re.search(pattern, query.upper())
        if match:
            return match.group(0)
        return None
    
    def _extract_company_symbol(self, query: str) -> Optional[str]:
        """Extract company stock symbol for SEC filings"""
        # Look for uppercase ticker symbols (3-5 letters)
        import re
        pattern = r'\b[A-Z]{2,5}\b'
        matches = re.findall(pattern, query)
        
        # Filter out common words that might match
        exclude = {'SEC', 'EDGAR', 'AND', 'FOR', 'THE', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'HAD', 'BY', 'HOT', 'BUT', 'SHE', 'CAN', 'YES', 'HOW', 'ITS', 'WHO', 'DID', 'HAS', 'HAD', 'BUT', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'HAD', 'BY'}
        
        for match in matches:
            if match not in exclude and len(match) >= 2:
                return match
        
        return None
    
    def _extract_stock_symbol(self, query: str) -> Optional[str]:
        """Extract stock symbol for Alpha Vantage"""
        # Similar to company symbol extraction
        return self._extract_company_symbol(query)
    
    def _merge_results(self, storage_results: List[Dict], external_data: Dict[str, Any], intent: str) -> List[Dict]:
        """Merge Storage Facility results with external data"""
        merged = []
        
        # Add storage results first (your 30,657 entries)
        for result in storage_results:
            merged.append({
                'type': 'knowledge_base',
                'source': result.get('unit_name', 'storage_facility'),
                'topic': result.get('topic', ''),
                'content': result.get('content', '')[:500] + '...',
                'category': result.get('category', ''),
                'relevance': result.get('relevance', 0),
                'entry_id': result.get('entry_id', '')
            })
        
        # Inject external data at the top (when relevant)
        if 'crypto' in external_data:
            crypto = external_data['crypto']
            merged.insert(0, {
                'type': 'live_data',
                'source': 'CoinGecko API',
                'topic': f"{crypto['symbol'].title()} Live Price",
                'content': f"Current price: ${crypto['price_usd']:,.2f} USD ({crypto['change_24h']:+.2f}% 24h change). Data from {crypto['source']} at {crypto['timestamp']}",
                'category': 'cryptocurrency',
                'relevance': 1.0,
                'live': True
            })
        
        if 'cve' in external_data:
            cve = external_data['cve']
            cve_summary = f"Recent vulnerabilities from {cve['source']}: " + ', '.join([c['id'] for c in cve['recent_cves'][:3]])
            merged.insert(0, {
                'type': 'live_data',
                'source': 'NIST NVD',
                'topic': 'Recent Security Vulnerabilities',
                'content': cve_summary,
                'category': 'security',
                'relevance': 1.0,
                'live': True,
                'details': cve['recent_cves']
            })
        
        if 'wikipedia' in external_data:
            wiki = external_data['wikipedia']
            merged.insert(0, {
                'type': 'live_data',
                'source': 'Wikipedia',
                'topic': wiki['title'],
                'content': wiki['summary'],
                'category': 'reference',
                'relevance': 0.9,
                'live': True,
                'url': wiki['url']
            })
        
        return merged


# ========== MONITORING & METRICS ==========
class MetricsCollector:
    """Collect metrics without external dependencies (Prometheus optional)"""
    
    def __init__(self):
        self.metrics = defaultdict(int)
        self.response_times = []
        self.start_time = time.time()
    
    def increment(self, metric_name: str, value: int = 1):
        """Increment counter"""
        self.metrics[metric_name] += value
    
    def record_response_time(self, endpoint: str, duration_ms: float):
        """Record response time"""
        self.response_times.append({
            'endpoint': endpoint,
            'duration_ms': duration_ms,
            'timestamp': time.time()
        })
        
        # Keep only last 1000 entries
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        uptime = time.time() - self.start_time
        
        return {
            'uptime_seconds': round(uptime, 2),
            'total_requests': self.metrics.get('total_requests', 0),
            'successful_requests': self.metrics.get('successful_requests', 0),
            'failed_requests': self.metrics.get('failed_requests', 0),
            'external_api_calls': self.metrics.get('external_api_calls', 0),
            'cache_hits': self.metrics.get('cache_hits', 0),
            'cache_misses': self.metrics.get('cache_misses', 0),
            'avg_response_time_ms': round(
                sum(r['duration_ms'] for r in self.response_times) / len(self.response_times)
                if self.response_times else 0,
                2
            )
        }


# ========== SECURITY LAYER ==========
class SecurityCore:
    """Security features without modifying database"""
    
    def __init__(self):
        self.kill_switch_active = False
        self.suspicious_patterns = [
            r"(\bUNION\b.*\bSELECT\b)",  # SQL injection
            r"(--|\/\*|\*\/)",           # SQL comments
            r"(<script|javascript:)",    # XSS
            r"(\.\./|\.\.\\)",           # Path traversal
        ]
        self.request_counts = defaultdict(lambda: defaultdict(int))
        self.rate_limit = 100  # requests per minute per user
    
    def validate_query(self, query: str, user_id: str) -> Dict[str, Any]:
        """Validate query for security threats"""
        
        # Kill switch check
        if self.kill_switch_active:
            return {
                'valid': False,
                'reason': 'System temporarily locked - contact administrator'
            }
        
        # SQL injection detection
        for pattern in self.suspicious_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                logger.warning(f"Suspicious query from user {user_id}: {query}")
                return {
                    'valid': False,
                    'reason': 'Query contains potentially malicious patterns'
                }
        
        # Rate limiting (simple implementation)
        current_minute = int(time.time() / 60)
        if self.request_counts[user_id][current_minute] >= self.rate_limit:
            return {
                'valid': False,
                'reason': 'Rate limit exceeded. Please wait a moment.'
            }
        
        self.request_counts[user_id][current_minute] += 1
        
        return {'valid': True}
    
    def activate_kill_switch(self, reason: str):
        """Emergency system shutdown"""
        self.kill_switch_active = True
        logger.critical(f"KILL SWITCH ACTIVATED: {reason}")
    
    def deactivate_kill_switch(self):
        """Reactivate system"""
        self.kill_switch_active = False
        logger.info("Kill switch deactivated")


# ========== MAIN INTELLIGENCE LAYER ==========
class IntelligenceLayer:
    """
    Main intelligence wrapper around Storage Facility
    DOES NOT MODIFY DATABASE - only enhances queries and responses
    """
    
    def __init__(self, storage_facility_url='http://localhost:5003'):
        self.hybrid_search = HybridSearchEngine(storage_facility_url)
        self.security = SecurityCore()
        self.metrics = MetricsCollector()
        
        logger.info("Intelligence Layer initialized (Storage Facility preserved)")
    
    def intelligent_search(self, query: str, user_id: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Enhanced search with:
        - Intent classification
        - External data augmentation
        - Security validation
        - Performance monitoring
        
        Storage Facility remains UNTOUCHED
        """
        start_time = time.time()
        
        self.metrics.increment('total_requests')
        
        # 1. Security validation
        validation = self.security.validate_query(query, user_id)
        if not validation['valid']:
            self.metrics.increment('failed_requests')
            return {
                'success': False,
                'error': validation['reason']
            }
        
        try:
            # 2. Hybrid search (Storage + External)
            results = self.hybrid_search.search(query, user_id, max_results)
            
            # 3. Record metrics
            duration_ms = (time.time() - start_time) * 1000
            self.metrics.record_response_time('search', duration_ms)
            self.metrics.increment('successful_requests')
            
            return results
            
        except Exception as e:
            logger.error(f"Intelligence search failed: {e}")
            self.metrics.increment('failed_requests')
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        try:
            circuit_breakers = {
                name: breaker.state
                for name, breaker in self.hybrid_search.external_data.circuit_breakers.items()
            }
        except Exception as e:
            logger.error(f"Failed to get circuit breaker status: {e}")
            circuit_breakers = {'error': str(e)}
        
        return {
            'status': 'healthy' if not self.security.kill_switch_active else 'locked',
            'metrics': self.metrics.get_stats(),
            'circuit_breakers': circuit_breakers
        }
    
    def classify_intent(self, query: str) -> str:
        """Classify user intent using the intent classifier"""
        return self.hybrid_search.intent_classifier.classify(query)
    
    def aggregate_external_data(self, query: str) -> List[Dict[str, Any]]:
        """Aggregate external data for the query"""
        return self.hybrid_search.external_data.aggregate_data(query)


# Singleton instance
_intelligence_layer = None

def get_intelligence_layer(storage_url='http://localhost:3003') -> IntelligenceLayer:
    """Get singleton Intelligence Layer instance"""
    global _intelligence_layer
    if _intelligence_layer is None:
        _intelligence_layer = IntelligenceLayer(storage_url)
    return _intelligence_layer


# --- FLASK API WRAPPER ---
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

intelligence = None

def get_intelligence():
    global intelligence
    if intelligence is None:
        try:
            intelligence = get_intelligence_layer()
        except Exception as e:
            logger.error(f"Failed to initialize Intelligence Layer: {e}")
            raise
    return intelligence

@app.route('/health', methods=['GET'])
def health():
    try:
        return jsonify(get_intelligence().get_system_health())
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '')
        user_id = data.get('user_id', 'anonymous')
        max_results = int(data.get('max_results', 5))
        result = get_intelligence().intelligent_search(query, user_id, max_results)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print('Starting Intelligence API on port 5010...')
    app.run(host='localhost', port=5010, debug=False)
