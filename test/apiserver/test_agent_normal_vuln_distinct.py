######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_hardencode_vuln
# @created     : 星期六 12月 18, 2021 11:40:31 CST
#
# @description :
######################################################################

from test.apiserver.test_agent_base import AgentTestCase

from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


class AgentHardencodeTestCase(AgentTestCase):
    def test_agent_hardencode_vuln(self):
        json_ = {
            "detail": {
                "reqHeader": "c2VjLWZldGNoLW1vZGU6bmF2aWdhdGUKcmVmZXJlcjpodHRwOi8vbG9jYWxob3N0OjgwODAvc2lu\ray9zc3JmCnNlYy1mZXRjaC1zaXRlOnNhbWUtb3JpZ2luCmFjY2VwdC1sYW5ndWFnZTp6aC1DTix6\raDtxPTAuOCx6aC1UVztxPTAuNyx6aC1ISztxPTAuNSxlbi1VUztxPTAuMyxlbjtxPTAuMgpjb29r\raWU6SlNFU1NJT05JRD0yNDJCNzc5Q0VFMDgzQTBEODY2MThDQUYzRTIwRkYxRApkdC1zcGFuZGlk\rOjAKZG50OjEKZHQtdHJhY2VpZDo1ZmU0MTQ2NzA5MDc0NDQxYTFjODBkZjgzYjhmNmQwMC1kNjYz\rMGM2NDIzOGI0YmM2YTk3YzdiYWI4ZDRlZDQ2NS4yNC4xMTQuMC4wCnNlYy1mZXRjaC11c2VyOj8x\rCmFjY2VwdDp0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtx\rPTAuOSxpbWFnZS9hdmlmLGltYWdlL3dlYnAsKi8qO3E9MC44Cmhvc3Q6bG9jYWxob3N0OjgwODAK\rdXBncmFkZS1pbnNlY3VyZS1yZXF1ZXN0czoxCmNvbm5lY3Rpb246a2VlcC1hbGl2ZQphY2NlcHQt\rZW5jb2Rpbmc6Z3ppcCwgZGVmbGF0ZSwgYnIKdXNlci1hZ2VudDpNb3ppbGxhLzUuMCAoV2luZG93\rcyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjoxMDQuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8x\rMDQuMApzZWMtZmV0Y2gtZGVzdDpkb2N1bWVudAo=",
                "agentId": 24,
                "scheme": "http",
                "method": "GET",
                "appCaller": [
                    "java.lang.Thread.getStackTrace(Thread.java:1559)",
                    "io.dongtai.iast.core.utils.StackUtils.createCallStack(StackUtils.java:10)",
                    "io.dongtai.iast.core.handler.hookpoint.vulscan.normal.AbstractNormalVulScan.getLatestStack(AbstractNormalVulScan.java:59)",
                    "io.dongtai.iast.core.handler.hookpoint.vulscan.normal.CryptoBadMacVulScan.scan(CryptoBadMacVulScan.java:33)",
                    "io.dongtai.iast.core.handler.hookpoint.controller.impl.SinkImpl.solveSink(SinkImpl.java:39)",
                    "io.dongtai.iast.core.handler.hookpoint.SpyDispatcherImpl.collectMethodPool(SpyDispatcherImpl.java:499)",
                    "java.security.MessageDigest.getInstance(MessageDigest.java)",
                    "sun.security.provider.SecureRandom.init(SecureRandom.java:102)",
                    "sun.security.provider.SecureRandom.<init>(SecureRandom.java:79)",
                    "sun.reflect.GeneratedConstructorAccessor47.newInstance(Unknown Source)",
                    "sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)",
                    "java.lang.reflect.Constructor.newInstance(Constructor.java:423)",
                    "java.security.Provider$Service.newInstance(Provider.java:1689)",
                    "java.security.SecureRandom.getDefaultPRNG(SecureRandom.java:223)",
                    "java.security.SecureRandom.<init>(SecureRandom.java:163)",
                    "sun.security.ssl.JsseJce.getSecureRandom(JsseJce.java:285)",
                    "sun.security.ssl.SSLContextImpl.engineInit(SSLContextImpl.java:97)",
                    "javax.net.ssl.SSLContext.init(SSLContext.java:282)",
                    "org.apache.http.ssl.SSLContexts.createDefault(SSLContexts.java:52)",
                    "org.apache.http.impl.client.HttpClientBuilder.build(HttpClientBuilder.java:966)",
                    "org.apache.http.impl.client.HttpClients.createDefault(HttpClients.java:58)",
                    "iast.vuln.vul.SSRF.apacheHTTPClient(SSRF.java:70)",
                    "iast.vuln.controller.sink.SSRFController.apacheHTTPClientDomainPart(SSRFController.java:178)",
                    "sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)",
                    "sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)",
                    "sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)",
                    "java.lang.reflect.Method.invoke(Method.java:498)",
                    "org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:205)",
                    "org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:150)",
                    "org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:117)",
                    "org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:895)",
                    "org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:808)",
                    "org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)",
                    "org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1070)",
                    "org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:963)",
                    "org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006)",
                    "org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:898)",
                    "javax.servlet.http.HttpServlet.service(HttpServlet.java:655)",
                    "org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)",
                    "javax.servlet.http.HttpServlet.service(HttpServlet.java:764)",
                    "org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:227)",
                    "org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162)",
                    "org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53)",
                    "org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189)",
                    "org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162)",
                    "org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)",
                    "org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117)",
                    "org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189)",
                    "org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162)",
                    "org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)",
                    "org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117)",
                    "org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189)",
                    "org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162)",
                    "org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)",
                    "org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:117)",
                    "org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:189)",
                    "org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:162)",
                    "org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:197)",
                    "org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97)",
                    "org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:541)",
                    "org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:135)",
                    "org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)",
                    "org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78)",
                    "org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:360)",
                    "org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:399)",
                    "org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65)",
                    "org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:890)",
                    "org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1789)",
                    "org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)",
                    "org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191)",
                    "org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659)",
                    "org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)",
                    "java.lang.Thread.run(Thread.java:748)",
                ],
                "contextPath": "",
                "secure": False,
                "queryString": "domain=example.org&foo=www",
                "uri": "/sink/ssrf/unsafe/apache-httpclient-domain-part",
                "url": "http://localhost:8080/sink/ssrf/unsafe/apache-httpclient-domain-part",
                "protocol": "HTTP/1.1",
                "replayRequest": False,
                "resBody": "",
                "clientIp": "127.0.0.1",
                "reqBody": "",
                "resHeader": "",
                "vulnType": "crypto-bad-mac",
            },
            "type": 33,
        }
        strategy = IastStrategyModel.objects.filter(
            user_id=1, vul_type="crypto-bad-mac"
        ).first()
        if strategy:
            strategy.state == "enable"
            strategy.save()
        res1 = self.agent_report(json_)
        vul1 = IastVulnerabilityModel.objects.filter(strategy=strategy).first()
        self.assertEqual(res1.status_code, 200)
        res2 = self.agent_report(json_)
        self.assertEqual(res2.status_code, 200)
        vul2 = IastVulnerabilityModel.objects.filter(strategy=strategy).first()
        self.assertEqual(vul1.id, vul2.id)
