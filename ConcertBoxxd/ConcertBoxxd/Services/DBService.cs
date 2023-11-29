using ConcertBoxxd.Data;
using ConcertBoxxd.Services;
using System.Text.Json;
using System.Text;
using ConcertBoxxd.Services;

namespace ConcertBoxxd.Services
{
    public class DBService : FileAPIService
    {
        protected override string BASE_ADDR => "http://localhost:8000";
 
    }
}
