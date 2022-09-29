from cdsapi import Client
from cdsapi.api import Result
import json
import requests
import time

class ClientMultiRequest(Client):
    """ClientMultiRequest

    Extended cdsapi.Client that allows multiple request submissions.
    """
    def _api(self, url, request, method, multirequest=True):
        """_api 

        Most of the code is copied and altered from superclass cdsapi.Client,
        see [here]("https://github.com/ecmwf/cdsapi/blob/f3b94a9bc40f8d56b0d1ac8cc8bc84765509ef05/cdsapi/api.py#L247").
        Submit API request.

        Args:
            url (_type_): _description_
            request (_type_): _description_
            method (_type_): _description_

        Returns:
            cdsapi.api.Result: Result wrapper of the request
        """        

        self._status(url)

        if multirequest : session = requests.Session()
        session = self.session

        self.info("Sending request to %s", url)
        self.debug("%s %s %s", method, url, json.dumps(request))

        if method == "PUT":
            action = session.put
        else:
            action = session.post

        result = self.robust(action)(
            url, json=request, verify=self.verify, timeout=self.timeout
        )

        if self.forget:
            return result

        reply = None

        try:
            result.raise_for_status()
            reply = result.json()
        except Exception:

            if reply is None:
                try:
                    reply = result.json()
                except Exception:
                    reply = dict(message=result.text)

            self.debug(json.dumps(reply))

            if "message" in reply:
                error = reply["message"]

                if "context" in reply and "required_terms" in reply["context"]:
                    e = [error]
                    for t in reply["context"]["required_terms"]:
                        e.append(
                            "To access this resource, you first need to accept the terms"
                            "of '%s' at %s" % (t["title"], t["url"])
                        )
                    error = ". ".join(e)
                raise Exception(error)
            else:
                raise
        
        if not self.wait_until_complete:
            session.close()
            return Result(self, reply)

        return self.wait_for_completion(reply, session=session)
        
        
    def wait_for_completion(self, reply, limit_time=100,
                            session=requests.Session()):
        """wait_and_download _summary_

        Function that allows to wait for completion of request.

        Args:
            reply (dict): Reply of the HTTP request.
            limit_time (int, optional): Max time to wait in seconds. Defaults
                to 100.
            session: Request session. Defaults to new Session

        Returns:
            cdsapi.api.Result: Result wrapper of the request.
        """
        sleep = 1
        wait_time = 0

        while True:
            self.debug("REPLY %s", reply)

            if reply["state"] != self.last_state:
                self.info("Request is %s" % (reply["state"],))
                self.last_state = reply["state"]

            if reply["state"] == "completed":
                self.debug("Done")

                if "result" in reply:
                    return reply["result"]

                return Result(self, reply)

            if reply["state"] in ("queued", "running"):
                rid = reply["request_id"]

                self.debug("Request ID is %s, sleep %s", rid, sleep)
                time.sleep(sleep)
                
                # we track overall waiting time
                wait_time += sleep
                sleep *= 1.5
                if sleep > self.sleep_max:
                    sleep = self.sleep_max

                task_url = "%s/tasks/%s" % (self.url, rid)
                self.debug("GET %s", task_url)

                result = self.robust(self.session.get)(
                    task_url, verify=self.verify, timeout=self.timeout
                )
                result.raise_for_status()
                reply = result.json()
                
                # we exit the queue if request is still running though waiting
                if wait_time > limit_time : return reply
                continue

            if reply["state"] in ("failed",):
                self.error("Message: %s", reply["error"].get("message"))
                self.error("Reason:  %s", reply["error"].get("reason"))
                for n in (
                    reply.get("error", {})
                    .get("context", {})
                    .get("traceback", "")
                    .split("\n")
                ):
                    if n.strip() == "" and not self.full_stack:
                        break
                    self.error("  %s", n)
                raise Exception(
                    "%s. %s."
                    % (reply["error"].get("message"), reply["error"].get("reason"))
                )

            raise Exception("Unknown API state [%s]" % (reply["state"],))
        return
