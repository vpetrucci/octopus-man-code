/* CloudSuite1.0 Benchmark Suite
 * Copyright (c) 2011, Parallel Systems Architecture Lab, EPFL
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions 
 * are met:
 *
 *   - Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in 
 *     the documentation and/or other materials provided with the distribution.

 *   - Neither the name of the Parallel Systems Architecture Laboratory, 
 *     EPFL nor the names of its contributors may be used to endorse or 
 *     promote products derived from this software without specific prior 
 *     written permission.

 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
 * PARALLEL SYSTEMS ARCHITECTURE LABORATORY, EPFL BE LIABLE FOR ANY 
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
 * IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN 
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * Author: Stavros Volos
 */

package sample.searchdriver;

import com.sun.faban.driver.*;
import javax.xml.xpath.XPathExpressionException;
import java.io.*;
import java.util.Vector;
import java.util.logging.Logger;
import java.util.Random;

@BenchmarkDefinition (
    name    = "Sample Search Workload",
    version = "0.2",
    configPrecedence = true
)
@BenchmarkDriver (
    name           = "SearchDriver",
    threadPerScale    = 1
)
@FlatMix (
    operations = {"GET"},
    mix = { 100 },
    deviation = 0
)

@NegativeExponential (
    cycleType = CycleType.CYCLETIME,
    cycleMean = 2000,
    cycleDeviation = 50
)

public class SearchDriver {
    private DriverContext ctx;
    private HttpTransport http;
    String url;
    Random random = new Random();
    Vector<String> words = new Vector<String>();
    Vector<String> queries = new Vector<String>();
    String frontend, logFile, termsFile;

    public SearchDriver() throws XPathExpressionException, IOException {
        ctx = DriverContext.getContext();

	// Read the ip address and the port number of the frontend server
	frontend = "http://" +
		   ctx.getXPathValue("/searchBenchmark/serverConfig/ipAddress").trim() +
	 	   ":" +
		   ctx.getXPathValue("/searchBenchmark/serverConfig/portNumber").trim();

	// Read the path and the filename of the log in which the queries will be kept
	logFile = ctx.getXPathValue("/searchBenchmark/filesConfig/logFile").trim();
	//FileWriter fIN = new FileWriter(logFile);
        //BufferedWriter out = new BufferedWriter(fIN);
    	//out.write("Searched queries\n");
	//out.close();

	// Read the path and the filename of the terms which will be used to create the queries
	termsFile = ctx.getXPathValue("/searchBenchmark/filesConfig/termsFile").trim();
	FileInputStream fstream = new FileInputStream(termsFile);
	DataInputStream in = new DataInputStream(fstream);
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
  	String strLine;
    	while ((strLine = br.readLine()) != null) 
      	  words.add(strLine);
    	in.close();
	
        http = HttpTransport.newInstance();
    }
    @BenchmarkOperation (
        name    = "GET",
        max90th = 0.5,
        timing  = Timing.AUTO
    )
    public void doGet() throws IOException {
	int randomCard = random.nextInt(100);
	int termsSize = words.size();
	int queriesSize = queries.size();
	// Create the query
	String query=null;
	query = words.get(random.nextInt(termsSize));
	if (randomCard > 23){
		query = query + "+" + words.get(random.nextInt(termsSize));
		if (randomCard > 47){
			query = query + "+" + words.get(random.nextInt(termsSize));
			if (randomCard > 69){
				query = query + "+" + words.get(random.nextInt(termsSize));
				if (randomCard > 83){
					query = query + "+" + words.get(random.nextInt(termsSize));
					if (randomCard > 88){
						query = query + "+" + words.get(random.nextInt(termsSize));
						if (randomCard > 92){
							query = query + "+" + words.get(random.nextInt(termsSize));
							if (randomCard > 95){
								int j =random.nextInt(10);
								for (int i =0; i < j; i++)
									query = query + "+" + words.get(random.nextInt(termsSize));
							}
						}
					}
				}
			}
		}
	}
	// Create the http request
	//
	//url = frontend + "/solr/select/?q=articlePlainText%3A%22" + query + "%22&version=2.2&start=0&rows=100&indent=on&wt=json";
	//
	//url = frontend + "/search.jsp?query=" + query + "&lang=en";
	//url = frontend + "/my_river/my_type/_search?q=" + query;
	url = frontend + "/wiki/_search?q=" + query;

        //curl -XGET 'http://localhost:9200/wiki/_search?q=test'

	StringBuilder sb = http.fetchURL(url);
        String resp = sb.toString();
        String[] p1 = resp.split(",");
        String[] p2 = p1[0].split(":");
        String lat = p2[1];
        String tstamp = String.valueOf(System.currentTimeMillis() / 1000);
	FileWriter fstreamIN = new FileWriter(logFile,true);
        BufferedWriter out = new BufferedWriter(fstreamIN);
    	out.write(tstamp+","+query+","+lat+"\n");
	out.close();
	//http.fetchURL(url);
    }
}
