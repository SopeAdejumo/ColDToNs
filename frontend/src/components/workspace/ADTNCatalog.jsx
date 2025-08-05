import { useState, useEffect } from "react";
import axios from "axios";

const ADTNCatalog = () => {
  const [pulsarNames, setPulsarNames] = useState("");
  const [atnfParams, setAtnfParams] = useState([]);
  const [selectedParams, setSelectedParams] = useState([]);
  const [searchFilter, setSearchFilter] = useState("");
  const [selectAll, setSelectAll] = useState(false);
  const [loading, setLoading] = useState(false);
  const [queryResults, setQueryResults] = useState([]);
  const [queryParams, setQueryParams] = useState([]);
  const [showDownloadDropdown, setShowDownloadDropdown] = useState(false);

  useEffect(() => {
    // Fetch ATNF parameters from backend
    const fetchParams = async () => {
      try {
        const response = await axios.get("/api/atnf-parameters");
        setAtnfParams(response.data);
      } catch (error) {
        console.error("Failed to fetch ATNF parameters:", error);
      }
    };
    fetchParams();
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showDownloadDropdown && !event.target.closest('.download-dropdown')) {
        setShowDownloadDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDownloadDropdown]);

  const filteredParams = atnfParams.filter((param) =>
    param.toLowerCase().includes(searchFilter.toLowerCase())
  );

  const handleParamToggle = (param) => {
    setSelectedParams((prev) =>
      prev.includes(param) ? prev.filter((p) => p !== param) : [...prev, param]
    );
  };

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedParams([]);
    } else {
      setSelectedParams([...filteredParams]);
    }
    setSelectAll(!selectAll);
  };

  const handleDownload = async (format) => {
    try {
      const response = await axios.post("/api/tools/adtn-catalog/download", {
        data: queryResults,
        parameters: queryParams,
        format: format
      }, {
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Set filename based on format
      const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
      const filename = `atnf_catalog_${timestamp}.${format}`;
      link.setAttribute('download', filename);
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      setShowDownloadDropdown(false);
    } catch (error) {
      console.error("Download failed:", error);
    }
  };

  const handleQuery = async () => {
    setLoading(true);
    try {
      const response = await axios.post("/api/tools/adtn-catalog/data", {
        pulsarNames: pulsarNames
          .split(",")
          .map((name) => name.trim())
          .filter((name) => name),
        parameters: selectedParams,
      });
      
      // Manually parse the incoming string as an array
      let parsedResults = [];
      if (typeof response.data === 'string') {
        try {
          // Sanitize the JSON string by replacing NaN values with null
          const sanitizedData = response.data
            .replace(/:\s*NaN/g, ': null')
            .replace(/,\s*NaN/g, ', null')
            .replace(/\[\s*NaN/g, '[null')
            .replace(/NaN\s*\]/g, 'null]')
            .replace(/NaN\s*,/g, 'null,');
          
          parsedResults = JSON.parse(sanitizedData);
        } catch (parseError) {
          console.error("Failed to parse response data as JSON:", parseError);
          parsedResults = [];
        }
      } else if (Array.isArray(response.data)) {
        parsedResults = response.data;
      } else {
        parsedResults = response.data ? [response.data] : [];
      }
      
      setQueryResults(parsedResults);
      // Store the parameters used for this query to display in the table
      setQueryParams([...selectedParams]);
      // Handle the response data here
    } catch (error) {
      console.error("Query failed:", error);
      setQueryResults([]);
      setQueryParams([]);
    } finally {
      setLoading(false);
      // Reset pulsar names and selected parameters after query
      setPulsarNames("");
      setSelectedParams([]);
    }
  };

return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">ADTN Catalog</h2>
      <div className="space-y-4">
        {/* Pulsar Selection */}
        <div className="border border-gray-600 rounded-lg p-4">
          <label
            htmlFor="pulsar-jnames"
            className="block text-lg font-semibold mb-2"
          >
            Pulsar Selection
          </label>
          <textarea
            id="pulsar-jnames"
            rows="3"
            placeholder="J0534+2200, J1939+2134"
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2 resize-y"
            value={pulsarNames}
            onChange={(e) => setPulsarNames(e.target.value)}
          />
          <p className="text-sm text-gray-400 mb-2">
            Enter a comma-separated list of pulsar JNAMES (e.g., 'J0534+2200,
            J1939+2134'). Leave blank to query all pulsars.
          </p>
        </div>

        {/* Parameter Selection */}
        <div className="border border-gray-600 rounded-lg p-4">
          <label className="block text-lg font-semibold mb-2">
            Select Parameters
          </label>

          {/* Select All */}
          <div className="mb-2">
            <input
              type="checkbox"
              id="select-all-params"
              className="mr-2"
              checked={selectAll}
              onChange={handleSelectAll}
            />
            <label
              htmlFor="select-all-params"
              className="text-sm font-medium cursor-pointer"
            >
              Select All
            </label>
          </div>

          {/* Search Filter */}
          <input
            type="text"
            placeholder="Search parameters..."
            className="w-full p-2 border border-gray-600 rounded bg-gray-800 text-gray-100 mb-2"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
          />

          {/* Parameter List */}
          <div className="max-h-40 overflow-y-auto border border-gray-600 rounded bg-gray-900 p-2 space-y-1">
            {filteredParams.map((param) => (
              <div key={param}>
                <input
                  type="checkbox"
                  id={`param-${param}`}
                  value={param}
                  className="mr-2"
                  checked={selectedParams.includes(param)}
                  onChange={() => handleParamToggle(param)}
                />
                <label htmlFor={`param-${param}`} className="cursor-pointer">
                  {param}
                </label>
              </div>
            ))}
          </div>

          <p className="text-sm text-gray-400 mt-2">
            Choose the catalogue parameters to retrieve (e.g., JNAME, RAJ, DECJ,
            P0, DM).
          </p>

          {/* Query Button */}
          <button
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            onClick={handleQuery}
            disabled={loading || selectedParams.length === 0}
          >
            {loading ? "Querying..." : "Query Catalog"}
          </button>
        </div>
        {/* Result Display */}
        <div className="border border-gray-600 rounded-lg p-4 mt-4">
          <label className="block text-lg font-semibold mb-2">
            Query Results
          </label>

          {loading ? (
            <p className="text-gray-400">Loading results...</p>
          ) : !Array.isArray(queryResults) || queryResults.length === 0 ? (
            <p className="text-gray-400">No results to display.</p>
          ) : (
            /* Display the table with results */
            <div>
              {/* Download Button */}
              <div className="mb-4 relative download-dropdown">
                <button
                  onClick={() => setShowDownloadDropdown(!showDownloadDropdown)}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download
                  <svg className={`w-4 h-4 transition-transform ${showDownloadDropdown ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                {showDownloadDropdown && (
                  <div className="absolute top-full left-0 mt-1 bg-gray-800 border border-gray-600 rounded shadow-lg z-10">
                    <button
                      onClick={() => handleDownload('csv')}
                      className="block w-full text-left px-4 py-2 hover:bg-gray-700 text-white"
                    >
                      CSV
                    </button>
                    <button
                      onClick={() => handleDownload('json')}
                      className="block w-full text-left px-4 py-2 hover:bg-gray-700 text-white"
                    >
                      JSON
                    </button>
                    <button
                      onClick={() => handleDownload('xlsx')}
                      className="block w-full text-left px-4 py-2 hover:bg-gray-700 text-white"
                    >
                      Excel (XLSX)
                    </button>
                  </div>
                )}
              </div>
              
              <div className="overflow-x-auto">
                <table className="min-w-full border border-gray-700 text-sm">
                  <thead>
                    <tr>
                      {queryParams.map((param) => (
                        <th
                          key={param}
                          className="px-3 py-2 border-b border-gray-700 bg-gray-800 text-gray-100 font-semibold"
                        >
                          {param}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {queryResults.map((row, idx) => (
                      <tr key={idx} className="hover:bg-gray-800">
                        {queryParams.map((param) => (
                          <td
                            key={param}
                            className="px-3 py-2 border-b border-gray-700"
                          >
                            {row[param] === null || row[param] === undefined 
                              ? <span className="text-gray-500 italic">N/A</span>
                              : row[param]}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ADTNCatalog;